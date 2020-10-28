# AWS EKS CDK

A CDK deployment to create a VPC and EKS Cluster

This project is useful if you are looking to get started with an instance of Kodexa from AWS Marketplace. It will create
a VPC with an EKS cluster in place ready for the marketplace helm deployment.

In order to use this CDK project we recommend you create an IAM user specifically for the creation of this cluster, with specific
rights for EKS to enable Kodexa to be deployed.

## Creating an AWS IAM user

First let’s create an IAM user that we will use to manage this process.

In your AWS console goto the IAM section (https://console.aws.amazon.com/iam/home). Choose to add a new user.

![][image-1]

## Getting Started

```
conda env create -f environment.yml
conda activate kodexa_cdk
pip install -r requirements.txt

cdk deploy
```
Once finished

```
cdk destroy
```

[image-1]:	images/iam1.png