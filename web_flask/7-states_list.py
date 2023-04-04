#!/usr/bin/python3
''' starts flash app '''

# importing Flask task
from flask import Flask, render_template
from models import storage
from models.state import State

# instance of the class
app = Flask(__name__)


# route to tell what URL should trigger the function
@app.route('/states_list', strict_slashes=False)
def states_list():
    """ returns a list of all states in the Database """
    state_li = storage.all(State).values()
    return render_template('7-states_list.html', states=state_li)


# closes or otherwise deallocates the resource if it exists.
@app.teardown_appcontext
def teardown_appcontext(exception):
    """ closese session """
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
