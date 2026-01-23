#!/usr/bin/env bash
set -e

if [ $# -lt 1 ]; then
  echo "Usage: $0 <file-path>"
  exit 1
fi

FILE_PATH="$1"

mkdir -p "$(dirname "$FILE_PATH")"

cat > "$FILE_PATH" << 'EOF'
[DEFAULT]
themes_dirs = ["/usr/share/grub/themes"]
grub_file = /etc/default/grub
EOF

echo "Created file: $FILE_PATH"
