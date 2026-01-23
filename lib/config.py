import os
import shutil
import subprocess
from pathlib import Path

def get_editor():
    editor = os.environ.get("EDITOR")
    if editor:
        return editor.split()

    for cmd in ("nano", "vi", "vim", "micro"):
        path = shutil.which(cmd)
        if path:
            return [path]

    raise RuntimeError("No text editor found. Set $EDITOR.")


def open_config(path: Path):
    editor = get_editor()
    subprocess.run(editor + [str(path)], check=True)
