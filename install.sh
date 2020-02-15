mkdir weixinrobot
cd weixinrobot
apt install virtualenv
virtualenv venv
source venv/bin/activate
pip install flask
pip install requests
wget https://files.uniartisan.com/WXRobot.py
chmod +x WXRobot.py
chmod u+x remove.sh
clear
echo "Success! Please Please get your key and fill it in python source code"
echo "After editting, try:'nohup python WXRobot.py &' and visit http://127.0.0.1:5000"
nano WXRobot.py
