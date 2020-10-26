
# Add azure-cli repo
zypper install -y curl gcc gcc-c++ make ncurses patch wget tar zlib-devel zlib openssl-devel
rpm --import https://packages.microsoft.com/keys/microsoft.asc
zypper addrepo --name 'Azure CLI' --check https://packages.microsoft.com/yumrepos/azure-cli azure-cli
zypper refresh

# Download Python source code
PYTHON_VERSION="3.6.9"
PYTHON_SRC_DIR=$(mktemp -d)
wget -qO- https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz | tar -xz -C "$PYTHON_SRC_DIR"
# Build Python
# Please be aware that with --prefix=/usr, the command will override the existing python3 version
$PYTHON_SRC_DIR/*/configure --with-ssl --prefix=/usr
make
make install
# Download azure-cli package 
AZ_VERSION=$(zypper --no-refresh info azure-cli |grep Version | awk -F': ' '{print $2}' | awk '{$1=$1;print}')
wget https://packages.microsoft.com/yumrepos/azure-cli/azure-cli-$AZ_VERSION.x86_64.rpm
# Install without dependency
rpm -ivh --nodeps azure-cli-$AZ_VERSION.x86_64.rpm