#!/bin/bash

# DigitalOcean deployment script
# Requires doctl to be installed and configured

echo "Deploying to DigitalOcean App Platform..."

# Create the app using doctl
doctl apps create --spec .do/app.yaml

echo "Deployment initiated. Check your DigitalOcean dashboard for progress."