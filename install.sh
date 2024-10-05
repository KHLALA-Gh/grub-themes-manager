#!/bin/bash
SCRIPTPATH="$(readlink -f "$0")"
DIRNAME="$(dirname "$SCRIPTPATH")"
ENVDIR="$DIRNAME/.env"
if  [  -d "$ENVDIR" ]; then
  rm -rf $ENVDIR
fi

echo "# creating virtual environment..."
python3 -m venv $ENVDIR


echo "# activating virtual environment..."
source $ENVDIR/bin/activate
echo "installing pip packages"
pip install -r $DIRNAME/requirements.txt

python3 $DIRNAME/install.py
