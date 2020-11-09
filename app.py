#!/usr/bin/env python3

from aws_cdk import core

from kodexa_stacks.cluster import KodexaStack

app = core.App()

# Update this line to add your IAM username (ie. amadeapaula) to 
# the system administrators group for the cluster
iam_user = None

# This is the size of the initial node group for the cluster
default_capacity = 3

# If you want to use an existing VPC you can provide the VPC ID
# here
vpc_id=None

# The instance type to use for the node group
default_instance_type='t3a.large'

vpc_stack = KodexaStack(app, "primary", 
                        iam_user=iam_user, 
                        default_capacity=default_capacity, 
                        vpc_id=vpc_id, 
                        default_instance_type=default_instance_type)
app.synth()
