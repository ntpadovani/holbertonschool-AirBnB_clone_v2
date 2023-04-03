#!/usr/bin/python3
"""
A script that starts a Flask web application
"""

from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """Displays the message"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hello2():
    """Displays the message"""
    return "HBNB"


@app.route('/c/<text>')
def c_text(text):
    """Displays 'C' with the variable text"""
    return "C %s" % text.replace('_', ' ')


@app.route('/python/', defaults={'text': 'is cool'})
@app.route('/python/<text>')
def py_text(text):
    """Displays 'Python' with the variable text"""
    return "Python %s" % text.replace('_', ' ')


@app.route('/number/<int:n>')
def int_text(n):
    """Displays the variable 'n' only if it is an integer, in a message"""
    return "%d is a number" % n


@app.route('/number_template/')
@app.route('/number_template/<int:n>')
def num_template(n):
    """Displays a HTML page only if 'n' is an integer"""
    return render_template('5-number.html', num=n)

if __name__ == "__main__":
    app.run()
