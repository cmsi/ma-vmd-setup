#!/bin/sh

# Compile script for VMD written by Synge Todo

SOURCE="$1"
PREFIX="$2"
PREFIX=`(cd $PREFIX && pwd)`
SCRIPTDIR=`dirname $0`
SCRIPTDIR=`(cd $SCRIPTDIR && pwd)`
UNAME=$(uname -m)
if [ "$UNAME" = "x86_64" ]; then
  ARCH=LINUXAMD64
elif [ "$UNAME" = "i386" ]; then
  ARCH=LINUX
else
  echo "Error: unsupported architecture"
  exit 127
fi

if [ -z $PREFIX ]; then
  echo "Usage: $0 source_tarball prefix"
  exit 127
fi

BUILDDIR="$HOME/build"
PREFIX="$PREFIX"
VMDDIR="$PREFIX/share/vmd"

if [ -d "$VMDDIR" ]; then
  echo "Error: VMD directory exists ($VMDDIR)"
  exit 127
fi

# Extract files from the tarball
if [ -f "$SOURCE" ]; then :; else
  echo "Error: source not found ($SOURCE)"
  exit 127
fi
MD5SUM=`md5sum "$SOURCE" | awk '{print $1}'`
if [ "$MD5SUM" = "2f8835175a2f50515da9943808a81b1a" ]; then
  VERSION="1.9.2"
else
  echo "Error: unknown version or corrupted archive"
  exit 127
fi
echo "VMD version = $VERSION"
rm -rf $BUILDDIR/vmd-$VERSION $BUILDDIR/plugins
mkdir -p $BUILDDIR
echo "Extracting $SOURCE into $BUILDDIR"
tar zxvf "$SOURCE" -C "$BUILDDIR"
cd $BUILDDIR/vmd-$VERSION
mv ../plugins .

if [ -f "$SCRIPTDIR/vmd-$VERSION.patch" ]; then
  echo "Patching to source code"
  patch -p1 < "$SCRIPTDIR/vmd-$VERSION.patch"
fi

echo "Compiling plugins"
cd $BUILDDIR/vmd-$VERSION/plugins
make $ARCH
make distrib PLUGINDIR=$PREFIX/libexec/vmd/plugins

echo "Compiling VMD"
cd $BUILDDIR/vmd-$VERSION
VMDINSTALLBINDIR=$PREFIX/bin VMDINSTALLLIBRARYDIR=$PREFIX/libexec/vmd PLUGINDIR=$PREFIX/libexec/vmd ./configure LINUXAMD64 IMD LIBTACHYON NETCDF COLVARS TCL PTHREADS
cd src
make INCDIRS="-I/usr/include/tachyon -I/usr/include/tcl -I../plugins/include -I../plugins/LINUXAMD64/molfile -I../lib/netcdf/include -I$PREFIX/libexec/vmd/plugins/LINUXAMD64/molfile -I." LIBDIRS="-L$PREFIX/libexec/vmd/plugins/LINUXAMD64/molfile"

echo "Compilation Done"
