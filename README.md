# Purpose of this repository

This repository will be useful if you are looking to get started with an instance of Kodexa from AWS Marketplace. It
will create a VPC with an EKS cluster in place ready for the marketplace helm deployment.

Note: At the end of this document are two important items:

1. How to destroy the EKS cluster that you created (to stop spending $$)
1. The link you need to follow to deploy Kodexa to the EKS Cluster you will be creating.

In essence, the process is:

- install your Prerequisites for a AWS EKS deploy.
- deploy an AWS EKS clusters
- install Prerequisites for a Kodexa deploy
- deploy Kodexa into the AWS cluster

# Assumptions

1. The reader is familiar with GitHub
1. The user has an AWS user account with administrative permissions

# What is AWS EKS CDK?

A AWS CDK (Amazon Web Services Cloud Development Kit) deployment will be used to create the following for our
installation:

* VPC (Virtual Private Cloud)
* EKS Cluster (Amazon Elastic Kubernetes Service).
* 3 x S3 buckets (for storing assets, objects and caching)
* RDS Postgres database for metadata and data storage in Kodexa

## AWS Cloud Shell

Go to your AWS Console and from there search for Cloud Shell, and then launch an instance.

Once you have a Cloud Shell instance available you can simply run the following command to clone this repository to your
shell.

```bash
git clone https://github.com/kodexa-ai/aws-eks-cdk.git
cd aws-eks-cdk
./aws-shell-go.sh
```

This will download and setup all the tools you'll need to build a new VPC, EKS cluster, S3 buckets for storage and
caching and also an RDS instance to use as a database.

## Before the deploy commands, edit the app.py file  
Hint - open another duplicate tab so that you can see these instructions at the saem time a you edit the app.py file.

The CDK script itself is written in Python, and if you look at the app.py you will see that we pass in the name “demo”,
and we allow you to set your IAM name (to ensure you are a system administrator of the cluster).

**IMPORTANT: You MUST change the iam_user in app.py line 12. (for example: iam_user = "kodexa") to ensure you are a
system administrator of the cluster**

**Optional Advanced Options: Beyond adding your IAM user to provide you access to the cluster you can also edit the
app.py to change some other settings.**

```python
# This is the size of the initial node group for the cluster
default_capacity = 3

# If you want to use an existing VPC you can provide the VPC ID
# here (for example vpc-063ee4e387458dd5d).
# Note that if you are going to provide a VPC ID you will also have
# to provide the account (your AWS account ID) and the region
vpc_id = None  # or example 'vpc-063ee4e387458dd5d'
account = None  # or example '045323014440'
region = None  # or example  'us-east-1'

# The instance type to use for the node group
default_instance_type = 't3a.large'
```

If you have any questions please contact support@kodexa.com

### Time to deploy the cluster ###

You can now the deploy command:

This process will take some time,around 1/2 hour, to create the infrastructure. As stated directly above, the process will first show
you the changes that will be made before making them. **You will see a Y/N prompt fairly quickly in the process showing
the proposed changes. Press Y to continue.**
All CDK changes will be made through a CloudFormation template.

```bash 
cdk deploy
```

*If at any time your AWS Cloud Shell disconnects, return to the AWS Console and goto Cloud Formation to monitor your
stack's deployment*

At the end of the deploy, the command will **output** an AWS CLI command that will register the cluster with your local
kubectl.

```bash
Outputs:
demo.Output = vpc-066b33daxxxxxxxx
demo.kodexaeksclusterdemoConfigCommand8FA7EDC8 = aws eks update-kubeconfig --name kodexa-eks-cluster-demo --region us-east-1 --role-arn arn:aws:iam::045323014350:role/demo-kodexaeksadminroledemo56DDE46B-xxxxxxxx
demo.kodexaeksclusterdemoGetTokenCommand26EC227C = aws eks get-token --cluster-name kodexa-eks-cluster-demo --region us-east-1 --role-arn arn:aws:iam::045323014350:role/demo-kodexaeksadminroledemo56DDE46B-xxxxxxxxx

Stack ARN:
arn:aws:cloudformation:us-east-1:045323014350:stack/demo/84305320-1936-11eb-xxxx-xxxxxxxxx
```

If the session closed on you you can find this information in the CloudFormation Console, look for a stack with the name
you gave this Kodexa instance, choose it and then choose outputs.

**Be sure to copy this information as some of it is needed in subsequent steps.**

### Immediately after the deploy command finishes:

**Inside the Outputs, find the entire command that starts with "aws eks update-kubeconfig...".**


## Destroying the EKS cluster

You can run this again in your cloud shell

```bash
cdk destroy
```

**Note that you will be asked if you wish to delete the primary. Type Y. This process will take a while to complete as
did the 'cdk deploy'**

If you need help with any of these steps for working with EKS clusters for Kodexa come join us
in [Kodexa Slack](https://slack.kodexa.com) \[3\]

\[1\]:    https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html
