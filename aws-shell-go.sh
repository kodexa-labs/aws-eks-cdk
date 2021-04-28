#!/usr/bin/env bash

echo "Setting up for a CDK installation for Kodexa"
sudo npm install -g aws-cdk
sudo pip3 install -r requirements.txt
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod 755 kubectl
echo "Ok we have the basics installed, now run:"
echo "$ cdk deploy"