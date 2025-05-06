#!/usr/bin/env python3
from art import tprint
import os
import subprocess
from configparser import ConfigParser
from lib.colors import bcolors
from lib.print import iprint
import json
from distro import id
title=tprint("Grub Themes",font="small")

# Read and set config from config.ini file 
config_file_name = "./config.ini"
config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),config_file_name)
if not os.path.isfile(config_file_path) :
    iprint(f"config file does not exist '{config_file_name}'.",bcolors.FAIL,"ERROR")
    iprint(f"you can run {os.path.join(os.path.dirname(os.path.realpath(__file__)),"install.sh")} to generate default configs",bcolors.WARNING,"HINT")
    quit(1)
try :
    config = ConfigParser()
    config.read(config_file_path)
    default = config["DEFAULT"]
    grub_themes_paths=json.loads(default["themes_dirs"])
    grub_cfg_file_path = default["grub_file"]
    grub_cfg = default["grub_cfg"]
    for i in range (len(grub_themes_paths)) :
        if not os.path.isdir(grub_themes_paths[i]) :
            raise NotADirectoryError(f": {grub_themes_paths[i]} is not a directory in themes_dirs")
except Exception as e :
    iprint(f"An error occurred when parsing the config file :",bcolors.FAIL,"ERROR")
    print (type(e).__name__,e)
    iprint(f"you can run {os.path.join(os.path.dirname(os.path.realpath(__file__)),"install.sh")} to generate default configs",bcolors.WARNING,"HINT")
    quit()

# Read themes from themes directories
content = []

for i in range(len(grub_themes_paths)) :
    dirs = os.listdir(grub_themes_paths[i])
    for j in range(len(dirs)) :
        if os.path.isfile(os.path.join(grub_themes_paths[i],dirs[j],"theme.txt")) :
            content.append(os.path.join(grub_themes_paths[i],dirs[j]))
res=""
tab="\t"
nl="\n"
print(f"themes found in {' '.join(grub_themes_paths)}")
print("Choose a grub theme :\n")
t_names = []
for i in range (len(content)) :
    tn = content[i].split('/')[::-1][0]
    if not tn in t_names :
        t_names.append(tn)
    else :
        tn+= f" ({content[i]})"
    if i == 0 :
        res = f"{i+1}) {tn}"
        continue
    res += f"{ tab*2 if i % 3 else nl*2}{i+1}) {tn}"
print(res)
test = False
while test == False :
    inp=input(f"write theme number [1-{len(content)}]('c' to quit) : ")
    if inp.isdigit() and 0 < int(inp) < len(content)+ 1: 
       test = True 
    elif inp.lower()=="c" :
        quit(0)
    else :
        print(f"please type a number between 1 and {len(content)}")
theme_index = int(inp) - 1
theme_path = content[theme_index]
print(theme_path)
theme_name = content[theme_index].split('/')[::-1][0]
print(f"installing {theme_name}...")

# edit the grub config file


def change_theme(file_path,theme_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove lines containing GRUB_THEME
    new_lines = [line for line in lines if 'GRUB_THEME=' not in line]
    new_lines.append(f'GRUB_THEME="{os.path.join(theme_path,"theme.txt")}"')
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
       file.writelines(new_lines)


change_theme(grub_cfg_file_path,theme_path)
grubConfigCmd = "grub-mkconfig"

if id() == "fedora" :
    grubConfigCmd = "grub2-mkconfig"
# generate the grub config file
result = subprocess.run(f"sudo {grubConfigCmd} -o {grub_cfg}",shell=True, check=True, stdout=subprocess.PIPE, text=True)
print(nl*3)
# finish 
print(theme_name,"is installed. Reboot to test the theme.")