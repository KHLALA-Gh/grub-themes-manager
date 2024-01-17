#!/usr/bin/env python3

from art import tprint
import os
import subprocess
title=tprint("Grub Themes",font="small")

grub_themes_path="/boot/grub/themes"
content = os.listdir(grub_themes_path)
dirs = []
for i in range (len(content)) :
    if  os.path.isdir(grub_themes_path+"/"+content[i]) :
        if os.path.isfile(grub_themes_path+"/"+content[i] +"/theme.txt") :
            dirs.append(content[i])
if len(dirs) == 0 :
    print(f"no theme detected in {grub_themes_path}")
    quit()     
res=""
tab="\t"
nl="\n"
print("Choose a grub theme :\n")
for i in range (len(dirs)) :
    if i == 0 :
        res = f"{i+1}) {dirs[i]}"
        continue
    res += f"{ tab*2 if i % 3 else nl*2}{i+1}) {dirs[i]}"

print(res)
test = False
while test == False :
    inp=input(f"write theme number [1-{len(dirs)}] : ")
    if inp.isdigit() and 0 < int(inp) < len(dirs)+ 1: 
       test = True 
    else :
        print(f"please type a number between 1 and {len(dirs)}")
theme_index = int(inp) - 1
theme_path = grub_themes_path + "/" + dirs[theme_index] + "/theme.txt"
theme_name = dirs[theme_index]
print(f"installing {theme_name}...")



# edit the grub config file


def remove_grub_theme_lines(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove lines containing GRUB_THEME
    new_lines = [line for line in lines if 'GRUB_THEME=' not in line]
    new_lines.append(f'GRUB_THEME="{theme_path}"')
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
       file.writelines(new_lines)


grub_cfg_file_path = "/etc/default/grub"

remove_grub_theme_lines(grub_cfg_file_path)

result = subprocess.run("sudo grub-mkconfig -o /boot/grub/grub.cfg",shell=True, check=True, stdout=subprocess.PIPE, text=True)
print(nl*5)
print(theme_name,"is installed. Reboot to test the theme.")