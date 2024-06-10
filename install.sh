#!/bin/bash
SCRIPTPATH="$(readlink -f "$0")"
DIRNAME="$(dirname "$SCRIPTPATH")"
ENVDIR="$DIRNAME/.env"
if  [ ! -d "$ENVDIR" ]; then
  echo "# creating virtual environment..."
  python3 -m venv $ENVDIR
fi


echo "# activating virtual environment..."
source $ENVDIR/bin/activate
echo "installing pip packages"
pip install -r $DIRNAME/requirements.txt
clear
python3 $DIRNAME/install.py
