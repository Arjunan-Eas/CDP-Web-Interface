from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    text1 = request.form['clientId']
    text2 = request.form['topic']
    text3 = request.form['message']
    text4 = str(datetime.now())[:10]
    text5 = str(datetime.now())[11:19]
    with open('/home/ubuntu/webapp/messaging/message.txt', 'w') as f:
        f.write(f'DUID:{text1}\nTOPIC:{text2}\nDATA:{text3}\nDATE:{text4}\nTIME:{text5}')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='10.42.0.1')
