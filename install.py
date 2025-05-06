#!/usr/bin/env python3

# dont run this file. use install.sh !
from distro import id
from art import tprint
from lib.colors import bcolors
from lib.print import iprint
from lib.shell_init_file import get_shell_rc
import json
import configparser
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
iprint("generating configs",bcolors.WARNING,"RUN")

grubCmd = "grub"
if id() == "fedora" :
    grubCmd = "grub2"

themesDirs = ["/usr/share/grub/themes"]
if os.path.isdir(f"/boot/{grubCmd}/themes") :
    themesDirs.append(f"/boot/{grubCmd}/themes")


config = configparser.ConfigParser()

config["DEFAULT"] = {
    "themes_dirs" : json.dumps(themesDirs),
    "grub_file" : "/etc/default/grub",
    "grub_cfg" : f"/boot/{grubCmd}/grub.cfg"
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)

alias_name = '"grub-tm"'

start_command = f"sudo {os.path.join(dirname,'.env/bin/python3')} {os.path.join(dirname,'main.py')}"
alias_syntax = f"alias {alias_name}='{start_command}'"


shellName ,rc_file = get_shell_rc()
if shellName : 
    iprint(f"detected {shellName} shell",bcolors.OKGREEN,"INFO")
else :
    iprint(f"couldn't detected shell",bcolors.FAIL,"ERROR")

if not rc_file or not os.path.isfile(rc_file) :
    iprint(f"couldn't detect init file for {shellName}",bcolors.FAIL,"ERROR")
    while not os.path.isfile(os.path.expanduser(rc_file)) :
        rc_file = input("write your initialization file : ")




config_file_path = os.path.expanduser(rc_file)

iprint(f"adding {alias_name} to {rc_file}",bcolors.OKGREEN,"INFO")
check = check_alias_existence(config_file_path,alias_name)
if check :
    iprint(f"{alias_name} already exists in {config_file_path} as an alias.",bcolors.FAIL,"ERROR")
    quit(1)

with open(config_file_path,"r+") as file :
    content = file.read()
    file.write("\n"+alias_syntax)

iprint("refreshing the shell",bcolors.OKGREEN,"INFO")
subprocess.run(["source",rc_file],shell=True)

iprint("The installation is successfully completed !",bcolors.OKCYAN,"COMPLETED")
op=input("\n do you like to open grub theme manager ? (y/n) : ")
if op.upper() != "Y" :
    quit(0)
print(f"> {alias_name}")
subprocess.run(start_command,shell=True)