from flask import Flask, render_template, request, redirect, url_for
from flask import render_template_string
from datetime import datetime
import json

app = Flask(__name__)
first_message = True


@app.route('/')
def index():
    # return render_template('index.html')
    with open('new_index.html', 'r') as f:
        return render_template_string(f.read())

@app.route('/submit', methods=['POST'])
def submit():
    global first_message
    if first_message:
        open("message_history.txt", "w").close()
        first_message = False
    text1 = request.form['DUID']
    text2 = request.form['TOPIC']
    text3 = request.form['DATA']
    text4 = str(datetime.now())[:10]
    text5 = str(datetime.now())[11:19]
    # with open('/home/ubuntu/webapp/messaging/message.txt', 'w') as f:
    with open('message.txt', 'w') as f:
        f.write(f'DUID:{text1}\nTOPIC:{text2}\nDATA:{text3}\nDATE:{text4}\nTIME:{text5}')
    with open("message_history.txt", "a") as f:
        f.write(json.dumps({'DUID':text1, 'TOPIC': text2, 'DATA' : text3, 'DATE' : text4, 'TIME' : text5}))
    return redirect(url_for('index'))

@app.route('/page_reloaded', methods=['POST'])
def page_reloaded():
    global first_message
    first_message = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    # app.run(host='10.42.0.1')
    app.run()