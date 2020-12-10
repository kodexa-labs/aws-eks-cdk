# AWS EKS CDK

A CDK deployment to create a VPC and EKS Cluster

This project is useful if you are looking to get started with an instance of Kodexa from AWS Marketplace. It will create a VPC with an EKS cluster in place ready for the marketplace helm deployment.

## Getting Started

First up, install CDK on your machine, see [Getting started with the AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) \[1\]. Note that during your AWS configure you will be using the access and secret keys we received from creating the user above. **Use us-east-1 as the region.**  For Windows users, be sure to add the entries and values for 


AWS_ACCESS_KEY = AKIAI44QH8DHBEXAMPLEKEY  
AWS_SECRET_ACCESS_KEY = je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLESECRETKEY   
AWS_REGION = us-EAST-1  


To use CDK we recommend that you [install Anaconda](https://www.anaconda.com/products/individual) \[2\]. You can then create the conda environment and use that to manage the dependencies. Using Github, clone this repository locally.  Then, in Anaconda Prompt, point to the directory of the repository and run the following commands:

```bash
conda env create -f environment.yml
conda activate kodexa_cdk
pip install -r requirements.txt
```

Now you have your environment available.

## Deploying the EKS cluster

The CDK script itself is written in Python, and if you look at the app.py you will see that we pass in the name “demo”, and we allow you to set your IAM name (to ensure you are a system administrator of the cluster).

You *MUST* change the iam_user in app.py (for example: iam_user = "kodexa") and if you wish to give the VPC and cluster a more meaningful name you can change "demo".

### Additional Settings

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

Then you can run the deploy command. This is done in Anaconda Prompt - make sure you are in this conda environment/directory before running the deploy code:

```bash
cdk deploy
```

This process willt take some time to create the infrastructure. Note it will first show you the changes that will be made before making them.

All CDK changes will be made through a CloudFormation template.

At the end of the deploy, the command will output an AWS CLI command that will register the cluster with your local kubectl. Make sure to run the command that starts with "aws eks update-kubeconfig..." before using Helm to deploy Kodexa.

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

You can also use the CDK command to destroy the environment that was created.

```bash
cdk destroy
```

If you need help with any of these steps for working with EKS clusters for Kodexa come join us in [Kodexa Slack](https://slack.kodexa.com) \[3\]

\[1\]:	https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html

\[2\]:	https://www.anaconda.com/products/individual

\[3\]:	https://slack.kodexa.com
