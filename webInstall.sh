sudo apt install python3-pip

sudo rm README.md
sudo rm -r Archive

cd webapp
python3 -m venv env
pip install redis
pip install flask
pip install flask-socketio

