#!/usr/bin/env python3

from aws_cdk import core

from kodexa_stacks.cluster import KodexaStack

app = core.App()
vpc_stack = KodexaStack(app, "demo")
app.synth()
