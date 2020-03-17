#!/usr/bin/env bash

set -ev
sleep 60
pip install azure-cli==$CLI_VERSION

ACTUAL_VERSION=$(az version | sed -n 's|"azure-cli": "\(.*\)",|\1|p' | sed 's|[[:space:]]||g')
echo "actual version:${ACTUAL_VERSION}"
echo "expected version:${CLI_VERSION}"

if [ "$ACTUAL_VERSION" != "$CLI_VERSION" ]; then
    echo "Latest package is not in the repo."
    exit 1
else
    echo "Latest package is verified."
fi