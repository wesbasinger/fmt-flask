from time import time
from datetime import datetime
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

@app.route('/lookup', methods=['GET'])
def get_lookup():

    cast = db.get_cast()

    return render_template('lookup.html', cast=cast)

@app.route('/lookup', methods=['POST'])
def post_lookup():

    cast_id = request.form.get('cast-member')

    cast = db.get_single_cast(cast_id)

    transformed = {
        "first_name" : cast['first_name'],
        "last_name" : cast['last_name'],
        "session" : cast['session'],
        "logs" : [],
        "total_hours" : 0
    }

    for log in cast['logs']:

        if log['time_out']:

            formatted = {
                "worker" : log['worker'],
                "time_in" : datetime.fromtimestamp(log['time_in']).strftime('%Y-%m-%d %H:%M:%S'),
                "time_out" : datetime.fromtimestamp(log['time_out']).strftime('%Y-%m-%d %H:%M:%S'),
                "logged_time" : round(((log['time_out'] - log['time_in']) / (60*60)), 1)
            }

            transformed['total_hours'] += formatted['logged_time']

            transformed['logs'].append(formatted)


    return render_template('cast-detail.html', cast=transformed)

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
