import os
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client.fmt_workday

cast = db.cast

def create_cast(first_name, last_name, session):

    new_cast = {
        "first_name" : first_name,
        "last_name" : last_name,
        "session" : session,
        "logs" : []
    }

    result = cast.insert_one(new_cast)

    print(result)

def get_cast():

    cursor = cast.find()

    results = []

    for res in cursor:

        res['_id'] = str(res['_id'])

        results.append(res)

    return results

def punch_in(cast_id, worker, ts):

    result = db.cast.update_one(
        {'_id' : ObjectId(cast_id)},
        {
            '$push' : {
                'logs' : { "time_in" : ts, "worker" : worker}
            }
        }
    )

    print(result)
