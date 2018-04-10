"""Not empty"""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    """Not empty"""
    return 'Hello World!'

if __name__ == '__main__':
    # this is a long line this is a long line this is a long line this is a
    # long line this is a long line
    app.run()
