import base64

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_eks as eks
import aws_cdk.aws_iam as iam
import aws_cdk.aws_rds as rds
import yaml
from aws_cdk import core
from aws_cdk.core import CfnParameter, Stack, SecretValue


def base64_encode_string(value):
    value_bytes = value.encode("ascii")
    base64_bytes = base64.b64encode(value_bytes)
    return base64_bytes.decode("ascii")


class KodexaStack(Stack):

    def __init__(self, scope, id, *, description=None, env=None, tags=None, synthesizer=None, iam_user=None):
        super().__init__(scope, id, description=description, env=env, tags=tags,
                         synthesizer=synthesizer)

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

        core.CfnOutput(self, "Output",
                       value=vpc.vpc_id)

        # Create K8S cluster

        cluster_admin = iam.Role(self, f"kodexa-eks-adminrole-{id}", assumed_by=iam.AccountRootPrincipal())

        cluster = eks.Cluster(self, id=f'kodexa-eks-cluster-{id}', cluster_name=f'kodexa-eks-cluster-{id}',
                              version=eks.KubernetesVersion.V1_17,
                              vpc=vpc,
                              default_capacity=4,
                              masters_role=cluster_admin)

        if iam_user:
            admin_user = iam.User.from_user_name(id='cluster-admin-iam-user', user_name=iam_user, scope=self)
            cluster.aws_auth.add_user_mapping(admin_user, groups=['system:masters'])
