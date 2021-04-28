#!/usr/bin/env bash

echo "Setting up for a CDK installation for Kodexa"
sudo npm install -g aws-cdk
sudo pip3 install -r requirements.txt

echo "Ok we have the basics installed, now run:\n"
echo "cdk deploy"