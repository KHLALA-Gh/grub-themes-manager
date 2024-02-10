#!/usr/bin/env python3

# dont run this file. use install.sh !

from art import tprint
from lib.colors import bcolors
from lib.print import iprint
import os
import subprocess
from lib.search_alias import check_alias_existence
tprint("Install")

print("\n\n\n")
print("install script will install the necessary packages and create an alias to use Grub Theme Manager")

dirname = os.path.dirname(os.path.realpath(__file__))

ask=input("start installation (Y/n): ")
if ask.upper() != "Y" :
    iprint("Installation canceled",bcolors.WARNING,"ABORTED")
    quit()

iprint("Starting the installation",bcolors.OKGREEN,"INFO")
alias_name = '"grub-tm"'

start_command = f"source {os.path.join(dirname,'.env/bin/activate')} && sudo python3 {os.path.join(dirname,'main.py')}"
alias_syntax = f"alias {alias_name}='{start_command}'"

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
op=input("\n do you like to open grub theme manager ? (y/n) : ")
if op.upper() != "Y" :
    quit(0)
print(f"> {alias_name}")
subprocess.run(start_command,shell=True)