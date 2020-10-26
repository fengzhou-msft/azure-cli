yum install gcc gcc-c++ make ncurses patch wget tar zlib zlib-devel -y

# build openssl from source
SRC_DIR=$(mktemp -d)
wget -qO- https://www.openssl.org/source/openssl-1.1.1d.tar.gz | tar -xz -C "$SRC_DIR"
cd $SRC_DIR/openssl-1.1.1d
./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl
make
make install
# configure shared object lookup directory so that libssl.so.1.1 can be found
echo "/usr/local/ssl/lib" | sudo tee /etc/ld.so.conf.d/openssl-1.1.1d.conf
# reload config
ldconfig -v

# build python from source
PYTHON_VERSION="3.6.9"
wget -qO- https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz | tar -xz -C "$SRC_DIR"
cd $SRC_DIR/Python-$PYTHON_VERSION
./configure --prefix=/usr --with-openssl=/usr/local/ssl
make
make install

# add azure-cli repo
rpm --import https://packages.microsoft.com/keys/microsoft.asc
sh -c 'echo -e "[azure-cli]
name=Azure CLI
baseurl=https://packages.microsoft.com/yumrepos/azure-cli
enabled=1
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/azure-cli.repo'

# download and install azure-cli
yum install yum-utils -y
yumdownloader azure-cli
rpm -ivh --nodeps azure-cli-*.rpm
