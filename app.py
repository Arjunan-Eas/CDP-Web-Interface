from flask import Flask, render_template, request, redirect, url_for
# from flask import render_template_string
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    # with open('index.html', 'r') as f:
    #     return render_template_string(f.read())

@app.route('/submit', methods=['POST'])
def submit():
    text1 = request.form['DUID']
    text2 = request.form['TOPIC']
    text3 = request.form['DATA']
    text4 = str(datetime.now())[:10]
    text5 = str(datetime.now())[11:19]
    with open('/home/ubuntu/webapp/messaging/message.txt', 'w') as f:
    # with open('message.txt', 'w') as f:
        f.write(f'DUID:{text1}\nTOPIC:{text2}\nDATA:{text3}\nDATE:{text4}\nTIME:{text5}')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='10.42.0.1')
    # app.run()
