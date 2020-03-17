#!/usr/bin/env bash

set -ev

ACTUAL_VERSION=$(docker run --rm mcr.microsoft.com/azure-cli az version | sed -n 's|"azure-cli": "\(.*\)",|\1|p' | sed 's|[[:space:]]||g')

echo "actual version:${ACTUAL_VERSION}"
echo "expected version:${CLI_VERSION}"

if [ "$ACTUAL_VERSION" != "$CLI_VERSION" ]; then
    echo "Latest package is not in the repo."
    exit 1
else
    echo "Latest package is verified."
fi
