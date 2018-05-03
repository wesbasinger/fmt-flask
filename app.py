from time import time
from flask import Flask, redirect, url_for, request, render_template

import db

app = Flask(__name__)

@app.route('/')
def index():

    cast = db.get_cast()

    return render_template('index.html', cast=cast)

@app.route('/add-cast', methods=['GET'])
def add_cast():

    return render_template('add-cast.html')

@app.route('/add-cast', methods=['POST'])
def post_cast():

    first_name = (request.form.get('first-name'))
    last_name = (request.form.get('last-name'))
    session = (request.form.get('session'))

    result = db.create_cast(first_name, last_name, session)

    return render_template('index.html')

@app.route('/sign-in', methods=['GET'])
def get_sign_in():

    cast = db.get_cast()

    return render_template('sign-in.html', cast=cast)


@app.route('/sign-in', methods=['POST'])
def post_sign_in():

    worker = request.form.get('worker')
    cast_id = request.form.get('cast-member')

    ts = time()

    db.punch_in(cast_id, worker, ts)

    cast = db.get_cast()

    return render_template('index.html', cast=cast)

@app.route('/sign-out', methods=['GET'])
def get_sign_out():

    actives = db.get_actives()

    return render_template('sign-out.html', actives=actives)

@app.route('/sign-out', methods=['POST'])
def post_sign_out():

    log_id = request.form.get('log-id')

    ts = time()

    db.punch_out(log_id, ts)

    cast = db.get_cast()

    return render_template('index.html', cast=cast)


'''
@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))
'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
