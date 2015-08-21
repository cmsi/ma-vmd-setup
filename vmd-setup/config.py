#! /usr/bin/python

import platform

base_url = "http://www.ks.uiuc.edu"
path = "Development/Download/download.cgi"
vmd_version = "1.9.2"
if platform.machine() == 'x86_64':
  archive_id = "1334"
  arch = "LINUXAMD64"
else:
  archive_id = "1333"
  arch = "LINUX"
tarball = "vmd-" + vmd_version + ".bin." + arch + ".opengl.tar.gz"

if __name__ == '__main__':
    print "base_url    =", base_url
    print "path        =", path
    print "vmd_version =", vmd_version
    print "archive_id  =", archive_id
    print "arch        =", arch
    print "tarball     =", tarball
