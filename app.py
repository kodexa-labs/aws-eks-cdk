#!/usr/bin/env python3

from aws-cdk import core
from asw_cdk.core import Environment

from kodexa_stacks.cluster import KodexaStack

app = core.App()

# Update this line to add your IAM username (ie. "kodexa") to
# the system administrators group for the cluster
iam_user = None

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

vpc_stack = KodexaStack(app, "primary",
                        iam_user=iam_user,
                        default_capacity=default_capacity,
                        vpc_id=vpc_id,
                        default_instance_type=default_instance_type,
                        env=Environment(account=account, region=region))
app.synth()
