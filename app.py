#!/usr/bin/env python3

from aws_cdk import core

from kodexa_stacks.cluster import KodexaStack

app = core.App()

# Update this line to add your IAM username (ie. amadeapaula) to 
# the system administrators group for the cluster
iam_user = None

vpc_stack = KodexaStack(app, "demo", iam_user=iam_user)
app.synth()
