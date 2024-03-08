#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives using the function do_clean
"""

from fabric.api import env, local, run, lcd
from datetime import datetime
from fabric.context_managers import cd
from fabric.operations import sudo
from fabric.operations import put
from fabric.operations import get

env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with actual IP addresses
env.user = 'ubuntu'  # Replace with actual username
env.key_filename = 'path/to/ssh/private/key'  # Replace with actual path to SSH private key

def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        number = int(number)
        if number < 0:
            number = 0

        with lcd("versions"):
            local("ls -t | tail -n +{} | xargs rm -f".format(number + 1))

        with cd("/data/web_static/releases"):
            run("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))

        return True
    except Exception as e:
        return False

