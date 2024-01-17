#!/usr/bin/env python3

# dont run this file. use install.sh !

from art import tprint
from lib.check_packages import is_package_installed
from lib.colors import bcolors
from lib.print import iprint
import os
import subprocess
from lib.search_alias import check_alias_existence
tprint("Install")

print("\n\n\n")
print("install script will install necessary packages and create an alias to use Grub Theme Manager")

required_packages = [
    "python-pip",
    "python3",
    "grub",
]

ask=input("start installation (Y/n): ")
if ask.upper() != "Y" :
    iprint("Installation canceled",bcolors.WARNING,"ABORTED")
    quit()

iprint("Starting the installation",bcolors.OKGREEN,"INFO")
iprint("checking necessary packages...",bcolors.OKGREEN,"INFO")
for i in range (len(required_packages)) :
    if not is_package_installed(required_packages[i]) :
        iprint(f"{required_packages[i]} package is not installed,{required_packages[i]} is required.",bcolors.FAIL,"ERROR")
        cont = input("continue anyway (y/N) : ")
        if cont.lower() != "y" :
            iprint("Installation canceled",bcolors.WARNING,"ABORTED")
            quit() 
alias_name = '"grub-tm"'


alias_syntax = f"alias {alias_name}='source {os.path.join(os.getcwd(),'.env/bin/activate')} && sudo python3 {os.path.join(os.getcwd(),'main.py')}'"

init_file = ""

while not os.path.isfile(os.path.expanduser(init_file)) :
    init_file = input("write your initialization file (default=~/.bashrc) : ")
    if not init_file :
        init_file = "~/.bashrc"

config_file_path = os.path.expanduser(init_file)

iprint(f"adding {alias_name} to {init_file}",bcolors.OKGREEN,"INFO")
check = check_alias_existence(config_file_path,alias_name)
if check :
    iprint(f"{alias_name} already exists in {config_file_path} as an alias.",bcolors.FAIL,"ERROR")
    quit(1)

with open(config_file_path,"r+") as file :
    content = file.read()
    file.write("\n"+alias_syntax)

iprint("refreshing the shell",bcolors.OKGREEN,"INFO")
subprocess.run(["source",init_file],shell=True)

iprint("The installation is successfully completed !",bcolors.OKCYAN,"COMPLETED")