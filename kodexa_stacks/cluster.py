import base64

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_eks as eks
import aws_cdk.aws_iam as iam
import aws_cdk.aws_rds as rds
import aws_cdk.aws_s3 as s3
from aws_cdk import core
from aws_cdk.core import RemovalPolicy, SecretValue, Stack


def base64_encode_string(value):
    value_bytes = value.encode("ascii")
    base64_bytes = base64.b64encode(value_bytes)
    return base64_bytes.decode("ascii")


class KodexaStack(Stack):

    def __init__(self, scope, id, *, description=None, env=None, tags=None, synthesizer=None, iam_user=None,
                 vpc_id=None, default_capacity=3, default_instance_type='t3a.xlarge', host_name=None):
        super().__init__(scope, id, description=description, env=env, tags=tags,
                         synthesizer=synthesizer)

        import yaml

        with open("resources/kodexa-chart.yaml", 'r') as stream:
            helm_values = yaml.safe_load(stream)

        if vpc_id:
            vpc = ec2.Vpc.from_lookup(self, "VPC",
                                      vpc_id=vpc_id)
        else:
            vpc = ec2.Vpc(self, f"kodexa-vpc-{id}",
                          max_azs=2,
                          cidr="10.10.0.0/16",
                          subnet_configuration=[ec2.SubnetConfiguration(
                              subnet_type=ec2.SubnetType.PUBLIC,
                              name="Public",
                              cidr_mask=24
                          ), ec2.SubnetConfiguration(
                              subnet_type=ec2.SubnetType.PRIVATE,
                              name="Private",
                              cidr_mask=24
                          )],
                          nat_gateways=1,
                          )

            core.CfnOutput(self, "vpcId",
                           value=vpc.vpc_id)

        # We need to create the namespace for kodexa and then
        # we will run the helm chart - overwriting YAML configuration with the RDS configuration
        # that we have in place

        # Create K8S cluster

        cluster_admin = iam.Role(self, f"kdxa-adminrole-{id}", assumed_by=iam.AccountRootPrincipal())

        eks_role = iam.Role(self, f"kdxa-eksrole-{id}",
                            role_name='eksRole',
                            assumed_by=iam.ServicePrincipal('eks.amazonaws.com')
                            )

        eks_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEKSServicePolicy'))
        eks_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEKSClusterPolicy'))

        cluster = eks.Cluster(self, id=f'kdxa-{id}', cluster_name=f'kodexa-{id}',
                              version=eks.KubernetesVersion.V1_17,
                              vpc=vpc,
                              role=eks_role,
                              default_capacity_instance=ec2.InstanceType(default_instance_type),
                              default_capacity=default_capacity,
                              masters_role=cluster_admin)

        if iam_user:
            admin_user = iam.User.from_user_name(id='cluster-admin-iam-user', user_name=iam_user, scope=self)

        cluster.aws_auth.add_user_mapping(admin_user, groups=['system:masters'])

        s3_cache_bucket = s3.Bucket(self, f"kodexa-cache-{id}", auto_delete_objects=True,
                                    removal_policy=RemovalPolicy.DESTROY,
                                    block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
        s3_storage_bucket = s3.Bucket(self, f"kodexa-storage-{id}", auto_delete_objects=True,
                                      removal_policy=RemovalPolicy.DESTROY,
                                      block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
        s3_assets_bucket = s3.Bucket(self, f"kodexa-assets-{id}", auto_delete_objects=True,
                                     removal_policy=RemovalPolicy.DESTROY,
                                     block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        cluster.default_nodegroup.role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["s3:*"]
        ))

        # Create RDS instance for database
        rds_database = rds.DatabaseInstance(
            self,
            id=f"kodexa-postgres-rds-{id}",
            database_name="kodexadb",
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            vpc=vpc,
            vpc_placement=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE
            ),
            security_groups=[cluster.cluster_security_group],
            credentials=rds.Credentials.from_password("kodexadb", SecretValue("kodexa!db")),
            multi_az=False,
            publicly_accessible=False,
            allocated_storage=100,
            storage_type=rds.StorageType.GP2,
            cloudwatch_logs_exports=[],
            deletion_protection=False,
            delete_automated_backups=True,
            backup_retention=core.Duration.days(7))

        helm_values['dharma']['platform']['environment'] = id
        helm_values['dharma']['platform']['assets']['bucketName'] = s3_assets_bucket.bucket_name
        helm_values['dharma']['platform']['cacheBucket'] = s3_cache_bucket.bucket_name
        helm_values['dharma']['platform']['storeBucket'] = s3_storage_bucket.bucket_name

        helm_values['dharma']['platform']['datasource'][
            'url'] = f"jdbc:postgresql://{rds_database.db_instance_endpoint_address}:{rds_database.db_instance_endpoint_port}/kodexadb"
        helm_values['dharma']['platform']['datasource']['username'] = "kodexadb"
        helm_values['dharma']['platform']['datasource']['password'] = "kodexa!db"

        if host_name is not None:

            # We need to add the policy for Amazon Load Balancer

            import json
            with open("resources/alb-policy.json", 'r') as stream:
                policy_json = json.load(stream)

            for statement_json in policy_json['Statement']:
                cluster.default_nodegroup.role.add_to_policy(iam.PolicyStatement.from_json(statement_json))

            helm_values['zen']['ingress']['enabled'] = True
            helm_values['zen']['ingress']['hosts'][0]['host'] = host_name
            helm_values['kodexa']['alb-ingress']['enabled'] = True

            helm_values['aws-load-balancer-controller']['clusterName'] = cluster.cluster_name

        import yaml
        core.CfnOutput(self, "helm-values",
                       value=yaml.dump(helm_values))

        cluster.add_helm_chart(id="kdxa", repository="https://charts.kodexa.com/internal", chart="kodexa",
                               create_namespace=True, namespace="kodexa", values=helm_values)
