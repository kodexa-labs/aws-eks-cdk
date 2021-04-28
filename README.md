
# Purpose of this repository
This repository will be useful if you are looking to get started with an instance of Kodexa from AWS Marketplace. It will create a VPC with an EKS cluster in place ready for the marketplace helm deployment.  

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
1. The user is an AWS user and has the AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY and knows the AWS region to be used.  We will use AWS_REGION = us-east-1 in this exercise.
1. The AWS account ID is known. You can get this while in the AWS console.  Click you user name on the upper right and you will see the account ID.

# What is AWS EKS CDK?
A AWS CDK (Amazon Web Services Cloud Development Kit) deployment will be used to create a VPC (Virtual Private Cloud) and EKS Cluster (Amazon Elastic Kubernetes Service).  We will then deploy Kodexa to the this managed Kubernetes Cluster.  

Amazon Elastic Kubernetes Service (EKS) is a managed Kubernetes service that makes it easy for you to run Kubernetes on AWS and on-premises. Amazon EKS is certified Kubernetes conformant, so existing applications that run on upstream Kubernetes are compatible with Amazon EKS).

It is assumed that the reader is familiar with GitHub.  

## AWS Cloud Shell

Go to your AWS Console and from there search for Cloud Shell, and then launch an instance.

Once you have a Cloud Shell instance available you can simply run the following command to clone this repository to your shell.

```bash
git clone https://github.com/kodexa-ai/aws-eks-cdk.git
cd aws-eks-cdk
./aws-shell-go.sh
```

This will download and setup all the tools you'll need to build a new VPC, EKS cluster, S3 buckets for storage and caching and also an RDS instance to use as a database.

## Before the deploy commands, edit the app.py file

The CDK script itself is written in Python, and if you look at the app.py you will see that we pass in the name “demo”, and we allow you to set your IAM name (to ensure you are a system administrator of the cluster).  

**IMPORTANT: You MUST change the iam_user in app.py line 12. (for example: iam_user = "kodexa") to ensure you are a system administrator of the cluster**

**IMPORTANT: You may need to change python3 to python on line 2 of cdk.json to reflect the name of the python executable you installed.**  Look in the directory that python was installed in and look for the executable's name (python, python39, etc.).

**Optional Advanced Options: Beyond adding your IAM user to provide you access to the cluster you can also edit the app.py to change some other settings.**

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
### Time to deploy the cluster ###
You can now the deploy command.   

``bash
cdk deploy
``

This process will take some time,around 1/2 hour, to create the infrastructure. Note that the process will first show you the changes that will be made before making them. **You will see a Y/N prompt fairly quickly in the process showing the proposed changes. Press Y to continue.**
All CDK changes will be made through a CloudFormation template.
At the end of the deploy, the command will **output** an AWS CLI command that will register the cluster with your local kubectl.
```bash
Outputs:
demo.Output = vpc-066b33daxxxxxxxx
demo.kodexaeksclusterdemoConfigCommand8FA7EDC8 = aws eks update-kubeconfig --name kodexa-eks-cluster-demo --region us-east-1 --role-arn arn:aws:iam::045323014350:role/demo-kodexaeksadminroledemo56DDE46B-xxxxxxxx
demo.kodexaeksclusterdemoGetTokenCommand26EC227C = aws eks get-token --cluster-name kodexa-eks-cluster-demo --region us-east-1 --role-arn arn:aws:iam::045323014350:role/demo-kodexaeksadminroledemo56DDE46B-xxxxxxxxx

Stack ARN:
arn:aws:cloudformation:us-east-1:045323014350:stack/demo/84305320-1936-11eb-xxxx-xxxxxxxxx

```
**Be sure to copy this information as some of it is needed in subsequent steps.**  
### Immediately after the deploy command finishes:

**Inside the Outputs, find the entire command that starts with "aws eks update-kubeconfig..." before using Helm to deploy Kodexa.**   
You can run this command from your open Anaconda Prompt. You will find the command after the = sign on the line that starts with "primary.kodexaeksclusterprimaryConfigCommand".  It will be a long string.
After this runs, you can verify it ran correctly by issuing the following command"
```bash
kubectl cluster-info
```

## IAM Permissions

If you are not running the CDK script with an AWS administrator role, then it is best to ensure you have the rights
needed. You can use the policy.json in this repository to provide you with the correct role for the deployment.

## Destroying the EKS cluster

You can also use the CDK command to destroy the environment that was created.  
**IMPORTANT: This is done in Anaconda Prompt - make sure you:**
1. **are in Anaconda Prompt**
2. **pointing to this repository before running the destroy code**
3. **note that each time you create a new Anaconda prompt, you need to activate the environment you intend to use. In the case, run the following commands.**

```bash
activate kodexa_cdk
cdk destroy
```

**Note that you will be asked if you wish to delete the primary. Type Y. This process will take a while to complete as did the 'cdk deploy'**

If you need help with any of these steps for working with EKS clusters for Kodexa come join us in [Kodexa Slack](https://slack.kodexa.com) \[3\]

\[1\]:	https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html

\[2\]:	https://www.anaconda.com/products/individual

\[3\]:	https://slack.kodexa.com

## Go on to deploy Kodexa into the cluster you have just created.
Go to https://developer.kodexa.com/learning-kodexa/deployment-options/#install-kubectl

Find  "Deployment Options" -> Install Kubectrl and proceed from there
