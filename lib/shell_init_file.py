import os
import shutil

def get_shell_rc():
    shell_path = os.environ.get("SHELL") or shutil.which("bash")  # fallback to bash
    shell_name = os.path.basename(shell_path)

    rc_file = None
    home_dir = os.path.expanduser("~")

    if shell_name == "bash":
        rc_file = os.path.join(home_dir, ".bashrc")
    elif shell_name == "zsh":
        rc_file = os.path.join(home_dir, ".zshrc")
    elif shell_name == "fish":
        rc_file = os.path.join(home_dir, ".config/fish/config.fish")

    return shell_name, rc_file

shell, rc_path = get_shell_rc()
