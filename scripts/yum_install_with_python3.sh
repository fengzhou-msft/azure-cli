#!/usr/bin/env bash
#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

#
# This script installs python 3 if not exist, then installs the latest azure-cli package without dependency.
# Use this script in step 3 of https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-yum?view=azure-cli-latest
# on a system with yum but without python 3.

yum install -y gcc gcc-c++ make ncurses patch wget tar zlib zlib-devel openssl-devel yum-utils

# Install python 3 if not exists
# Deafult location is /usr/local/bin/python, this script is invoked by sudo, 
# need to add the location to path when looking for python3 command as root
if ! PATH="$PATH:/usr/local/bin" command -v python3 >/dev/null 2>&1
then
    PYTHON_VERSION="3.6.5"
    PYTHON_SRC_DIR=$(mktemp -d)
    wget -qO- https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz | tar -xz -C "$PYTHON_SRC_DIR"
    # Build Python
    $PYTHON_SRC_DIR/*/configure
    make
    make install
fi
#Download azure-cli package
AZURE_CLI_PACKAGE_DIR=$(mktemp -d)
pushd ${AZURE_CLI_PACKAGE_DIR} > /dev/null
yumdownloader azure-cli
#Install without dependency
rpm -ivh --nodeps azure-cli-*.rpm
popd > /dev/null
rm -rf $PYTHON_SRC_DIR
rm -rf $AZURE_CLI_PACKAGE_DIR
