
echo "# activate virtual environment"
source .env/bin/activate
echo "installing pip packages"
pip install -r requirements.txt
clear
echo "# lunching install script..."
sleep 1
clear
python3 install.py
