#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers"""

from fabric.api import local, task
from os.path import isfile
from datetime import datetime
from pathlib import Path

env.hosts = ['xx-web-01', 'xx-web-02']
env.user = 'your_username'  # Replace with your username
env.key_filename = ['/path/to/your/private/key']

@task
def do_pack():
    """Generate a compressed archive from the web_static folder"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(archive_path))
    if result.failed:
        return None
    return archive_path

@task
def do_deploy(archive_path):
    """Deploy the archive to the web servers"""

    if not isfile(archive_path):
        return False

    try:
        # (Your previous do_deploy implementation here)
        # ...

        return True
    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False

@task
def deploy():
    """Create and distribute an archive to web servers"""

    # Call do_pack() to create an archive
    archive_path = do_pack()

    if not archive_path:
        return False

    # Call do_deploy() with the new archive path
    return do_deploy(archive_path)

