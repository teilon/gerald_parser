# gerald parser app
from flask import Flask
from parser import Wikipars

app = Flask(__name__)

@app.route('/')
def init():
    pars = Wikipars()
    pars.start()


if __name__ == '__main__':
    app.run(port=5000, debug=True)