#!/usr/bin/env bash

echo "Setting up for a CDK installation for Kodexa"
npm install aws-cdk
pip3 install -r requirements.txt

echo "Ok we have the basics installed, now run:\n"
echo "./node_modules/bin/cdk deploy"