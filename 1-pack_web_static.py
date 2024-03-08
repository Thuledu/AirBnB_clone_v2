#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of web_static
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        time_format = "%Y%m%d%H%M%S"
        time = datetime.utcnow().strftime(time_format)
        file_name = "versions/web_static_{}.tgz".format(time)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        return None
