#!/usr/bin/python2

import platform

base_url = "http://www.ks.uiuc.edu"
path = "Development/Download/download.cgi"
if platform.machine() == 'x86_64':
  vmd_version = "1.9.3"
  archive_id = "1475"
  arch = "LINUXAMD64-CUDA8-OptiX4-OSPRay111p1"
else:
  vmd_version = "1.9.2"
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
