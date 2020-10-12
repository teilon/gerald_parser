# gerald parser app
from flask import Flask
from parser import start

app = Flask(__name__)

@app.route('/')
def home():
    people = start()
    # data = list(map(p['name'] for p in people))
    data = []
    for p in people:
        data.append(p)

    return {'people': data}


if __name__ == '__main__':
    app.run(port=5000, debug=True)