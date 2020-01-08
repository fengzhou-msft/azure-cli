#!/usr/bin/env bash

# This script should be run in a docker to verify installing rpm package from the yum repository.

rpm --import https://packages.microsoft.com/keys/microsoft.asc
sh -c 'echo -e "[azure-cli]
name=Azure CLI
baseurl=https://packages.microsoft.com/yumrepos/azure-cli
enabled=1
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/azure-cli.repo'

yum install azure-cli

ACTUAL_VERSION=$(az version | sed -n 's|"azure-cli": "\(.*\)",|\1|p' | sed 's|[[:space:]]||g')
echo "actual version:${ACTUAL_VERSION}"
echo "expected version:${CLI_VERSION}"

if [ "$ACTUAL_VERSION" != "$CLI_VERSION" ]; then
    echo "Latest package is not in the repo."
    exit 1
else
    echo "Latest package is verified."
fi