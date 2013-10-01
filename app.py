from flask import Flask
from flask import render_template
from flask import jsonify

from cocaine.services import Service

app = Flask(__name__)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/info/<name>')
def info(name):
    try:
        return jsonify(Service(name).info().get())
    except Exception as err:
        return jsonify({"error": "information about specified application isn't available"})

if __name__ == "__main__":
    app.run(debug=True)
