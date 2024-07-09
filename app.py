from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    text1 = request.form['clientId']
    text2 = request.form['message']
    with open('/home/ubuntu/webapp/messaging/message.txt', 'w') as f:
        f.write(f'ClientID: {text1}\nMessage: {text2}')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='10.42.0.1')
