# gerald parser app
from flask import Flask
from parser import Wikipars

app = Flask(__name__)

@app.route('/')
def init():
    target_uri = 'https://ru.wikipedia.org/wiki/%D0%9C%D0%B8%D0%BB%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D1%81%D0%BA%D0%B0%D1%8F,_%D0%9C%D0%B0%D1%80%D0%B8%D1%8F_%D0%98%D0%BB%D1%8C%D0%B8%D0%BD%D0%B8%D1%87%D0%BD%D0%B0'
    pars = Wikipars()
    pars.start(target_uri)

    return 'Hello, Gerald!'


if __name__ == '__main__':
    app.run(port=5000, debug=True)