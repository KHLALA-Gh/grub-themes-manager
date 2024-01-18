<h1 align="center">Grub Theme Manager</h1>

## What is Grub Theme Manager ?
A program written in Python, its goal is to manage GRUB themes.
The program reads the themes stored in `/boot/grub/theme`, then waits for user input to choose a theme. Afterward, it edits the `GRUB_THEME` variable in the `/etc/default/grub` file and generates the configurations with the `grub-mkconfig` command.
<center>
<img src="./imgs/gtm.png" />
</center>

## required packages

python : https://www.python.org/ <br>
python-pip : https://pypi.org/project/pip/ <br>
grub : use your package manager to install GRUB. <br>

> **Note**: Before you start downloading the project, you need to make sure that you have the required packages installed in your system.


## Setup
### Download the project
```
$ git clone https://github.com/KHLALA-Gh/grub-themes-manager.git
```
### installation
cd to the repo :
```
$ cd ./grub-themes-manager
```
run install.sh script
```
$ ./install.sh
```
### post installation
run Grub Themes Manager :
```
$ grub-tm
```