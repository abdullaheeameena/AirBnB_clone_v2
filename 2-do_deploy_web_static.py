#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import env, put, run
import os

env.hosts = ['xx-web-01', 'xx-web-02']
env.user = 'your_username'  # Replace with your username
env.key_filename = ['/path/to/your/private/key']

def do_deploy(archive_path):
    """Deploy the archive to the web servers"""

    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/
        archive_filename = os.path.basename(archive_path)
        release_folder = '/data/web_static/releases/{}'.format(
            os.path.splitext(archive_filename)[0])
        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_folder))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents of web_static/ to the release folder
        run('mv {}/web_static/* {}'.format(release_folder, release_folder))

        # Remove the web_static folder
        run('rm -rf {}/web_static'.format(release_folder))

        # Remove the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {} /data/web_static/current'.format(release_folder))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False

