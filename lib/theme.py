import os
import shutil
import subprocess


def find_grub_update_command():
    # Debian / Ubuntu (preferred)
    if shutil.which("update-grub"):
        return ["update-grub"], None

    # Fedora / RHEL
    if shutil.which("grub2-mkconfig"):
        return ["grub2-mkconfig"], "/boot/grub2/grub.cfg"

    # Generic fallback
    if shutil.which("grub-mkconfig"):
        return ["grub-mkconfig"], "/boot/grub/grub.cfg"

    raise RuntimeError("No GRUB config generator found")

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


def install_theme(file_path,theme_path) : 
    change_theme(file_path,theme_path)

    cmd, output = find_grub_update_command()

    if output:
        cmd += ["-o", output]

    result = subprocess.run(
    cmd,
    check=True,
    stdout=subprocess.PIPE,
    text=True
    )

    if result.stderr :
        print(result.stderr)