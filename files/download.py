#!/usr/bin/python3

# Download script for VMD written by Synge Todo

import os
import sys
import mechanize
import subprocess

import config

def Download(username, password, targetdir):
    if (not os.path.isdir(targetdir)):
        os.mkdir(targetdir)
    try:
        br = mechanize.Browser()

        print("Accessing to " + config.base_url + " ...")
        br.open(config.base_url + "/" + config.path + "?UserID=&AccessCode=&ArchiveID=" + config.archive_id)
        br.select_form(nr = 1)
        br["UserName"] = username
        br["Password"] = password
        print("Submitting username and password...")
        response = br.submit()

        br.select_form(nr = 3)
        response = br.submit()

        req = br.find_link(text='this link')
        archive = req.url.split('/').pop()
        print("Retrieving " + archive + " ...")
        cmd = ['wget', '--output-document=' + targetdir + "/" + archive, config.base_url + req.url]
        p = subprocess.check_call(cmd)
        print("Done.")
    except:
        print("Error occurs. Download failed.")
        return 127
    return 0

if __name__ == '__main__':
    if (len(sys.argv) != 4):
        print("Usage:", sys.argv[0], "username", "password", "target_directory")
        sys.exit(127)
    username = sys.argv[1]
    password = sys.argv[2]
    targetdir = sys.argv[3]
    ret = Download(username, password, targetdir)
    sys.exit(ret)
