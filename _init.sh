#!/bin/bash

if [ ! -e _superman ]; then
	echo "virtualenv(python3): _superman"
	virtualenv -p python3 _superman
else
	echo "virtualenv(python) _superman already exists"
fi

[ -e _data ] || mkdir _data

cd ./_data
MANVER=man-pages-4.16
if [ ! -f ${MANVER}.tar.gz ]; then
	echo "wget ${MANVER}.tar.gz ...."
	wget https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/${MANVER}.tar.gz
else
	echo "${MANVER}.tar.gz has already been downloaded"
fi

if [ ! -e ${MANVER} ]; then
	tar xzvf ${MANVER}.tar.gz > /dev/null
else
	echo "files has already been extracted"
fi

if [ ! -e _0 ]; then
	mkdir _0
	for i in `seq 1 8`; do
		cp -rf ${MANVER}/man$i ./_0/man$i
	done
else
	echo "directory _0 already exists"
fi
