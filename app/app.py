# gerald parser app
from flask import Flask
from parser import start, Wikipars

app = Flask(__name__)

@app.route('/45')
def home():
    people = start()
    # data = list(map(p['name'] for p in people))
    data = []
    for p in people:
        data.append(p)

    return {'people': data}

@app.route('/')
def init():
    pars = Wikipars()
    pars.start()


if __name__ == '__main__':
    app.run(port=5000, debug=True)