#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers using the function deploy
"""

from fabric.api import local, env
from os.path import exists
from datetime import datetime
from fabric.operations import run, put
from fabric.context_managers import cd

env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with actual IP addresses
env.user = 'ubuntu'  # Replace with actual username
env.key_filename = 'path/to/ssh/private/key'  # Replace with actual path to SSH private key

def do_pack():
    """
    Generates a .tgz archive from the contents of web_static
    """
    try:
        if not exists("versions"):
            local("mkdir -p versions")
        time_format = "%Y%m%d%H%M%S"
        time = datetime.utcnow().strftime(time_format)
        file_name = "versions/web_static_{}.tgz".format(time)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        return None

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

def deploy():
    """
    Creates and distributes an archive to web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

