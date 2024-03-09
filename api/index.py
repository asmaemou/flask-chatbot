from flask import Flask


app = Flask(__name__)

@app.route('/ask_asmae', methods=['POST'])
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'
