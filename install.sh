#!/usr/bin/env bash
set -e

TOOL_NAME="grub-tm"
INSTALL_DIR="/opt/$TOOL_NAME"
VENV_DIR="$INSTALL_DIR/venv"
BIN_PATH="/usr/local/bin/$TOOL_NAME"
CONFIG_PATH="$INSTALL_DIR/config.ini"
echo "Installing $TOOL_NAME..."

# Must be run as root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root (use sudo)"
  exit 1
fi

# Detect Debian-based distro
if [ -f /etc/os-release ]; then
  . /etc/os-release
else
  echo "❌ Cannot detect OS"
  exit 1
fi

IS_DEBIAN=false
if [[ "$ID" == "debian" || "$ID_LIKE" == *"debian"* ]]; then
  IS_DEBIAN=true
fi

# Install python3-venv if Debian-based
if [ "$IS_DEBIAN" = true ]; then
  echo "Detected Debian-based system"

  if ! dpkg -s python3-venv >/dev/null 2>&1; then
    echo "Installing python3-venv..."
    apt update
    apt install -y python3-venv
  else
    echo "python3-venv already installed"
  fi
else
  echo "Non-Debian system detected (skipping python3-venv install)"
fi

# Install project files
echo "Installing files to $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
rsync -a --exclude '.git' ./ "$INSTALL_DIR/"
chmod +x $INSTALL_DIR/scripts/*
cat << EOF > "$CONFIG_PATH"
[DEFAULT]
themes_dirs = ["/usr/share/grub/themes"]
grub_file = /etc/default/grub
EOF

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv "$VENV_DIR"

# Install dependencies if requirements.txt exists
if [ -f "$INSTALL_DIR/requirements.txt" ]; then
  echo "Installing Python dependencies..."
  "$VENV_DIR/bin/pip" install --upgrade pip
  "$VENV_DIR/bin/pip" install -r "$INSTALL_DIR/requirements.txt"
fi

# Create launcher
echo "Creating launcher..."
cat << EOF > "$BIN_PATH"
#!/usr/bin/env bash
exec sudo $INSTALL_DIR/venv/bin/python3 $INSTALL_DIR/main.py "\$@"
EOF


chmod +x "$BIN_PATH"

echo
echo "✅ Installation complete!"
echo "➡ Run with: $TOOL_NAME"
