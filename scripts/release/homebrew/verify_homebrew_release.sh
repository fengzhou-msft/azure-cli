#!/usr/bin/env bash
set -ev

if brew list --versions azure-cli > /dev/null; then
  # The package is installed
  brew update
  brew upgrade azure-cli
else
  # The package is not installed
  brew install azure-cli
fi

ACTUAL_VERSION=$(az version | sed -n 's|"azure-cli": "\(.*\)",|\1|p' | sed 's|[[:space:]]||g')
echo "actual version:${ACTUAL_VERSION}"
echo "expected version:${CLI_VERSION}"

if [ "$ACTUAL_VERSION" != "$CLI_VERSION" ]; then
    echo "Latest package is not in the repo."
    exit 1
else
    echo "Latest package is verified."
fi