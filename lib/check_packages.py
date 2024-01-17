# Check system packages

import subprocess

def is_package_installed(package_name):
    try:
        subprocess.check_output(["pacman", "-Q", package_name])
        return True
    except subprocess.CalledProcessError:
        return False