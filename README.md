
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
1. Administrative rights to the PC being used to run this exercise.

# What is AWS EKS CDK?
A AWS CDK (Amazon Web Services Cloud Development Kit) deployment will be used to create a VPC (Virtual Private Cloud) and EKS Cluster (Amazon Elastic Kubernetes Service).  We will then deploy Kodexa to the this managed Kubernetes Cluster.  

Amazon Elastic Kubernetes Service (EKS) is a managed Kubernetes service that makes it easy for you to run Kubernetes on AWS and on-premises. Amazon EKS is certified Kubernetes conformant, so existing applications that run on upstream Kubernetes are compatible with Amazon EKS).

It is assumed that the reader is familiar with GitHub.  

## CDK Prerequisites
Several other programs / toolkits will be installed and used. References and links to relevant pages are provided.  

First up, install CDK on your machine, see [Getting started with the AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) \[1\].

Note that during your AWS configure you will be using the access and secret keys you received when your AWS was created. **Use us-east-1 as the region.**  

As described in the above link, if you are a Windows user, be sure to add the entries and values to your user path. Alternatively, you could use Windows Credential Manager. Here is an example.

AWS_ACCESS_KEY = AKIAI44QH8DHBEXAMPLEKEY  
AWS_SECRET_ACCESS_KEY = je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLESECRETKEY   
AWS_REGION = us-east-1  

1. To use CDK please [install Anaconda](https://www.anaconda.com/products/individual) \[2\].
1. Using Github, clone this repository locally using GitHub and note the directory the repository is in.
1. We will now create the conda environment and use that to manage the dependencies. **Using Anaconda Prompt**, change to the directory of the repository and run the following commands:
```bash
conda env create -f environment.yml
conda activate kodexa_cdk
pip install -r requirements.txt
```

You now have your conda environment available.

## Deploying the EKS cluster

The CDK script itself is written in Python, and if you look at the app.py you will see that we pass in the name “demo”, and we allow you to set your IAM name (to ensure you are a system administrator of the cluster).  
### Additional Settings (Optional. It is suggested you keep the default the first time you do this.)
**You may need to change python3 to python on line 2 of cdk.json to reflect the name of the python executable you installed.**  Look in the directory that python was installed in and look for the executable's name (python, python39, etc.).

**You may want to change the iam_user in app.py (for example: iam_user = "kodexa") if you wish to give the VPC and cluster a more meaningful name**

Beyond adding your IAM user to provide you access to the cluster you can also edit the app.py to change
some other settings.

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
You can now the deploy command. **IMPORTANT: This is done in Anaconda Prompt - make sure you are in Anaconda Prompt and pointing to this repository before running the deploy code**:

```bash
cdk deploy
```

This process will take some time to create the infrastructure. Note it will first show you the changes that will be made before making them.

All CDK changes will be made through a CloudFormation template.

At the end of the deploy, the command will output an AWS CLI command that will register the cluster with your local kubectl.

1. **Be sure to copy this information as some of it is needed in subsequent steps.**  
1. **Make sure to run the command that starts with "aws eks update-kubeconfig..." before using Helm to deploy Kodexa.**

```bash
Outputs:
demo.Output = vpc-066b33daxxxxxxxx
demo.kodexaeksclusterdemoConfigCommand8FA7EDC8 = aws eks update-kubeconfig --name kodexa-eks-cluster-demo --region us-east-1 --role-arn arn:aws:iam::045323014350:role/demo-kodexaeksadminroledemo56DDE46B-xxxxxxxx
demo.kodexaeksclusterdemoGetTokenCommand26EC227C = aws eks get-token --cluster-name kodexa-eks-cluster-demo --region us-east-1 --role-arn arn:aws:iam::045323014350:role/demo-kodexaeksadminroledemo56DDE46B-xxxxxxxxx

Stack ARN:
arn:aws:cloudformation:us-east-1:045323014350:stack/demo/84305320-1936-11eb-xxxx-xxxxxxxxx

```

## IAM Permissions

If you are not running the CDK script with an AWS administrator role, then it is best to ensure you have the rights
needed. You can use the policy.json in this repository to provide you with the correct role for the deployment.

## Destroying the EKS cluster

You can also use the CDK command to destroy the environment that was created.**IMPORTANT: This is done in Anaconda Prompt - make sure you are in Anaconda Prompt and pointing to this repository before running the destroy code**

```bash
cdk destroy
```

If you need help with any of these steps for working with EKS clusters for Kodexa come join us in [Kodexa Slack](https://slack.kodexa.com) \[3\]

\[1\]:	https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html

\[2\]:	https://www.anaconda.com/products/individual

\[3\]:	https://slack.kodexa.com

## Go on to deploy Kodexa into the cluster you have just created.
Go to https://developer.kodexa.com/learning-kodexa/deployment-options/#install-kubectl

Find  "Deployment Options" -> Install Kubectrl and proceed from there
