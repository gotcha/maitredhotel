#! /bin/bash

INSTALL_DIR=${PREFIX-/var/zmq}

DEBIAN_FRONTEND=noninteractive apt-get update -y -q
DEBIAN_FRONTEND=noninteractive apt-get install -y -q --force-yes uuid-dev build-essential git-core libtool autotools-dev autoconf automake pkg-config unzip libkrb5-dev cmake

mkdir -p ${INSTALL_DIR}
cd ${INSTALL_DIR}
git clone --depth 1 https://github.com/jedisct1/libsodium.git
cd ${INSTALL_DIR}/libsodium
./autogen.sh
./configure
make
sudo make install
sudo ldconfig

cd ${INSTALL_DIR}
git clone --depth 1 https://github.com/zeromq/libzmq.git
cd ${INSTALL_DIR}/libzmq
./autogen.sh
./configure
make
sudo make install
sudo ldconfig

cd ${INSTALL_DIR}
git clone --depth 1 https://github.com/zeromq/czmq.git
cd ${INSTALL_DIR}/czmq
./autogen.sh
./configure
make
sudo make install
sudo ldconfig

cd ${INSTALL_DIR}
git clone --depth 1 git://github.com/zeromq/malamute.git
cd ${INSTALL_DIR}/malamute
./autogen.sh
./configure
make
sudo make install
sudo ldconfig
