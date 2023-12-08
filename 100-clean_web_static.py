#!/usr/bin/python3
"""Fabric script to delete out-of-date archives"""

from fabric.api import env, run, local, lcd, cd
from fabric.decorators import task
from pathlib import Path
from datetime import datetime

env.hosts = ['xx-web-01', 'xx-web-02']
env.user = 'your_username'  # Replace with your username
env.key_filename = ['/path/to/your/private/key']

@task
def do_clean(number=0):
    """Delete out-of-date archives"""

    try:
        number = int(number)
        if number < 0:
            return False

        # Local clean
        with lcd("versions"):
            local("ls -1t | tail -n +{} | xargs rm -rf".format(number + 1))

        # Remote clean on both web servers
        with cd("/data/web_static/releases"):
            run("ls -1t | tail -n +{} | xargs rm -rf".format(number + 1))

        return True
    except Exception as e:
        print("Clean failed: {}".format(str(e)))
        return False

