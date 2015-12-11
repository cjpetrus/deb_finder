#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os
import signal
import time

# mirror to prepend .deb files with
# SOURCE_URI = 'ftp.us.debian.org/debian'
# subprocess shell commands
DEB_CMD = "apt-get install --reinstall --print-uris -qq {} | cut -d\"'\" -f2"
ALT_DEB_CMD = 'apt-cache show {} | grep "Filename:" | cut -f 2 -d " "'

DPKG_QUERY_CMD = "dpkg-query -f '${binary:Package}\n' -W "


# fix this
def signal_handler(signal_param, frame):
    print 'Ctrl+C received... killing process'
    time.sleep(1)
    # uncaught exception on posix
    os.kill(signal_param.CTRL_C_EVENT, 0)




def run_shell_cmd(cmd):
    proc = subprocess.Popen(
        cmd,
        preexec_fn=os.setpgrp,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    out, error = proc.communicate()
    result = out.decode()
    if result:
        return result
    else:
        print error
        return False


def get_installed_packages():
    print 'Getting packages installed with aptitude.'
    apt_packages = run_shell_cmd(DPKG_QUERY_CMD)
    if apt_packages:
        return apt_packages.splitlines()
    else:
        print 'No packages installed with aptitude found.'
        return None


def get_deb_url(apt_package_name):
    print 'Finding .deb file for the package {}.'.format(apt_package_name, )
    deb_file = run_shell_cmd(DEB_CMD.format(apt_package_name))
    if deb_file:
        return deb_file
    else:
        print 'Unable to find .deb file for the package {}.'.format(apt_package_name, )
        return None


def init_deb_finder():
    apt_packages = get_installed_packages()
    deb_files = list()
    unfound_packages = list()
    if apt_packages:
        for pkg in apt_packages:
            try:
                deb = get_deb_url(pkg)
                deb_files.append({'package': pkg, 'deb': deb, })
            except:
                unfound_packages.append(pkg)
                pass
    return {'found': deb_files, 'unfound': unfound_packages, }

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    init_deb_finder()
