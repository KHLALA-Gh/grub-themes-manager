

#!/bin/bash

ENVDIR=".env"

if  [ ! -d "$ENVDIR" ]; then
  echo "# creating virtual environment..."
  python -m venv .env
fi


echo "# activating virtual environment..."
source .env/bin/activate
echo "installing pip packages"
pip install -r requirements.txt
clear
python3 install.py
