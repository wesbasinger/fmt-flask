from time import time
from datetime import datetime
from flask import Flask, redirect, url_for, request, render_template, make_response
import csv

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

    if result:

        message = "Add cast was successful.  You may now log hours."

    else:

        message = "Something went wrong.  Please contact site adminstrator."

    return render_template('confirm.html', message=message)

@app.route('/sign-in', methods=['GET'])
def get_sign_in():

    cast = db.get_cast()

    return render_template('sign-in.html', cast=cast)


@app.route('/sign-in', methods=['POST'])
def post_sign_in():

    worker = request.form.get('worker')
    cast_id = request.form.get('cast-member')
    comment = request.form.get('comment')

    ts = time()

    result = db.punch_in(cast_id, worker, ts, comment)

    if result:

        message = "Sign in was successful.  Happy workday!"

    else:

        message = "Something went wrong.  Please contact site adminstrator."

    return render_template('confirm.html', message=message)

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

        if 'time_out' in log:

            formatted = {
                "worker" : log['worker'],
                "time_in" : datetime.fromtimestamp(log['time_in']).strftime('%Y-%m-%d %H:%M:%S'),
                "time_out" : datetime.fromtimestamp(log['time_out']).strftime('%Y-%m-%d %H:%M:%S'),
                "logged_time" : round(((log['time_out'] - log['time_in']) / (60*60)), 1),
                "comment" : log['comment']
            }

            transformed['total_hours'] += formatted['logged_time']

            transformed['logs'].append(formatted)


    return render_template('cast-detail.html', cast=transformed)

@app.route('/sign-out', methods=['POST'])
def post_sign_out():

    log_id = request.form.get('log-id')

    ts = time()

    result = db.punch_out(log_id, ts)

    if result:

        message = "Sign out was successful.  You should be able to view logged hours."

    else:

        message = "Something went wrong.  Please contact site adminstrator."

    return render_template('confirm.html', message=message)

@app.route('/download')
def download_csv():

    # list of dictionaries
    data = db.get_all_data()

    if data == []:

        message = "No data to download."

        return render_template('confirm.html', message=message)

    csv = "Cast, Session, Worker, Time In, Time Out, Comment, Total Time\n"

    for record in data:

        csv += record['cast'] + ", "
        csv += record['session'] + ", "
        csv += record['worker'] + ", "
        csv += datetime.fromtimestamp(record['time_in']).strftime('%Y-%m-%d %H:%M:%S') + ", "
        csv += datetime.fromtimestamp(record['time_out']).strftime('%Y-%m-%d %H:%M:%S') + ", "
        csv += record['comment'] + ", "
        csv += str(round(record['total_time']/60, 2))
        csv += "\n"

    response = make_response(csv)
    cd = 'attachment; filename=data.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'

    return response


# if __name__ == "__main__":
#     app.run(host='0.0.0.0', debug=True)
