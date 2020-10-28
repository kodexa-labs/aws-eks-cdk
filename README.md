# AWS EKS CDK

A CDK deployment to create a VPC and EKS Cluster

This project is useful if you are looking to get started with an instance of Kodexa from AWS Marketplace. It will create
a VPC with an EKS cluster in place ready for the marketplace helm deployment.

In order to use this CDK project we recommend you create an IAM user specifically for the creation of this cluster, with specific
rights for EKS to enable Kodexa to be deployed.

## Creating an AWS IAM user

First let’s create an IAM user that we will use to manage this process.

In your AWS console goto the IAM section (https://console.aws.amazon.com/iam/home). Choose to add a new user.

![Creating User][image-1]

For this example we will call the user kodexa-eks and only provide programmatic access. 

### Setting the correct rights for your user

## Getting Started

First up install CDK on your machine, see [https://docs.aws.amazon.com/cdk/latest/guide/getting\_started.html][1]. Note that during your AWS configure you will be using the access and secret keys we received from creating the user above.

In order to use CDK we recommend that you install Anaconda ([https://www.anaconda.com/products/individual][2]), you can then create the conda environment and use that to manage the dependencies.

```bash
conda env create -f environment.yml
conda activate kodexa_cdk
pip install -r requirements.txt

```

Now you have your environment in 

Once finished

```bash
cdk destroy
```

[1]:	https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html
[2]:	https://www.anaconda.com/products/individual

[image-1]:	./images/iam1.png