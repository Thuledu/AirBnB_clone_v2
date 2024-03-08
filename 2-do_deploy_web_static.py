#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers using the function do_deploy
"""

from fabric.api import env, put, run, sudo
from os.path import exists
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with actual IP addresses
env.user = 'ubuntu'  # Replace with actual username
env.key_filename = 'path/to/ssh/private/key'  # Replace with actual path to SSH private key

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split('/')[-1]
        folder_name = file_name.split('.')[0]
        remote_path = "/tmp/{}".format(file_name)
        release_path = "/data/web_static/releases/{}".format(folder_name)

        put(archive_path, remote_path)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf {} -C {}".format(remote_path, release_path))
        run("rm {}".format(remote_path))
        run("mv {}/web_static/* {}".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        return True
    except Exception as e:
        return False

