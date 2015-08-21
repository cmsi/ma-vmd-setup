#!/bin/sh

# Compile script for VMD written by Synge Todo

SOURCE="$1"
PREFIX="$2"
PREFIX=`(cd $PREFIX && pwd)`
SCRIPTDIR=`dirname $0`
SCRIPTDIR=`(cd $SCRIPTDIR && pwd)`
BUILDDIR="$HOME/build"
UNAME=$(uname -m)
if [ "$UNAME" = "x86_64" ]; then
  ARCH=LINUXAMD64
elif [ "$UNAME" = "i686" ]; then
  ARCH=LINUX
else
  echo "Error: unsupported architecture"
  exit 127
fi

if [ -z $PREFIX ]; then
  echo "Usage: $0 source_tarball prefix"
  exit 127
fi

# Extract files from the tarball
if [ -f "$SOURCE" ]; then :; else
  echo "Error: source not found ($SOURCE)"
  exit 127
fi
MD5SUM=`md5sum "$SOURCE" | awk '{print $1}'`
if [ "$UNAME" = "x86_64" -a "$MD5SUM" = "ff8b8a761822ebbb9be0e9f450d123b0" ]; then
  VERSION="1.9.2"
elif [ "$UNAME" = "i686" -a "$MD5SUM" = "e14abdbf5b8062d657f2a9cb4004e37d" ]; then
  VERSION="1.9.2"
else
  echo "Error: unknown version, architecture mismatch, or corrupted archive"
  exit 127
fi
echo "VMD version = $VERSION"
rm -rf $BUILDDIR/vmd-$VERSION $BUILDDIR/plugins
mkdir -p $BUILDDIR
echo "Extracting $SOURCE into $BUILDDIR"
tar zxvf "$SOURCE" -C "$BUILDDIR"
cd $BUILDDIR/vmd-$VERSION

if [ -f "$SCRIPTDIR/vmd-$VERSION.patch" ]; then
  echo "Patching to source code"
  patch -p1 < "$SCRIPTDIR/vmd-$VERSION.patch"
fi

echo "Configuring VMD"
VMDINSTALLBINDIR=$PREFIX/bin VMDINSTALLLIBRARYDIR=$PREFIX/libexec/vmd PLUGINDIR=$PREFIX/libexec/vmd ./configure
echo "Installing VMD"
(cd src && make install)
