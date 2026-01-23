#!/usr/bin/env python3
from art import tprint
import os
import subprocess
from configparser import ConfigParser
from lib.colors import bcolors
from lib.print import iprint
import json
from distro import id
from pathlib import Path
import argparse
from lib.config import open_config 
from lib.theme import install_theme


config_file_name = "config.ini"
root = os.path.dirname(os.path.realpath(__file__))

config_file_path = os.path.join(root,config_file_name)
parser = argparse.ArgumentParser(
            description="Tool to install Grub themes."
)
parser.add_argument("-c", "--config", action="store_true",help="edit config file")
parser.add_argument("-g", "--generate-config", action="store_true",help="generate new configs")
parser.add_argument("-i", "--install-theme", help="Install theme from a specific directory")
args = parser.parse_args()

config_path = Path(config_file_path)

if args.config:
    open_config(config_path)
elif args.generate_config :
    script_path = os.path.join(root,"scripts/gen_config.sh")
    result = subprocess.run(["sudo",script_path,config_file_path], 
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True)
    if result.returncode != 0 : 
        print(result.stderr)
        quit(result.returncode)



# Read and set config from config.ini file 

if not os.path.isfile(config_file_path) :
    iprint(f"config file does not exist '{config_file_path}'.",bcolors.FAIL,"ERROR")
    iprint(f"you can run 'grub-tm -g' to generate default configs",bcolors.WARNING,"HINT")
    quit(1)
try :
    config = ConfigParser()
    config.read(config_file_path)
    default = config["DEFAULT"]
    grub_themes_paths=json.loads(default["themes_dirs"])
    grub_cfg_file_path = Path(default["grub_file"])
    if not grub_cfg_file_path.exists() :
        iprint(f"{grub_cfg_file_path} does not exist (the grub config file does not exist)",bcolors.FAIL,"ERROR")
        iprint(f"make sure the 'grub_file' path is correct in '{config_file_path}' (run 'grub-tm -c' to edit)",bcolors.WARNING,"HINT")
        quit(1)
    for i in range (len(grub_themes_paths)) :
        if not os.path.isdir(grub_themes_paths[i]) :
            raise NotADirectoryError(f": {grub_themes_paths[i]} is not a directory in themes_dirs")
except Exception as e :
    iprint(f"An error occurred when parsing the config file :",bcolors.FAIL,"ERROR")
    print (type(e).__name__,e)
    iprint(f"you can run 'grub-tm -g' to generate default configs",bcolors.WARNING,"HINT")
    quit(1)



if args.install_theme :
    if os.path.isdir(args.install_theme) :
        try : 
            if not os.path.isfile(os.path.join(args.install_theme,"theme.txt")) :
                iprint("not a theme directory (theme.txt does not exist)",bcolors.FAIL,"ERROR")
                quit(1)
            install_theme(grub_cfg_file_path,args.install_theme)
            quit(0)
        except : 
            quit(1)
    else : 
        iprint(f"{args.install_theme} : No such directory",bcolors.FAIL,"ERROR")
        quit(1)



title=tprint("Grub Themes",font="small")



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
    inp=input(f"write theme number [1-{len(content)}]('q' to quit) : ")
    if inp.isdigit() and 0 < int(inp) < len(content)+ 1: 
       test = True 
    elif inp.lower()=="q" :
        quit(0)
    else :
        print(f"please type a number between 1 and {len(content)}")
theme_index = int(inp) - 1
theme_path = content[theme_index]
print(theme_path)
theme_name = content[theme_index].split('/')[::-1][0]
print(f"installing {theme_name}...")

# edit the grub config file

try : 
    install_theme(str(grub_cfg_file_path),theme_path)
except(err) :
    print(err)
finally :
    # finish 
    print(theme_name,"is installed. Reboot to test the theme.")

