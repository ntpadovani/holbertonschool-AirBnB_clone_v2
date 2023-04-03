#!/usr/bin/python3
"""
A script that starts a Flask web application
"""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """Displays the message"""
    return "Hello HBNB!"

if __name__ == "__main__":
    app.run()
