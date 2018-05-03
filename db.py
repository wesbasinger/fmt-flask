import os
import uuid

from pymongo import MongoClient
from bson.objectid import ObjectId

'''
client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
'''

client = MongoClient('mongodb://admin:annie510@ds031661.mlab.com:31661/fmt')

db = client.fmt

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
                'logs' : { "time_in" : ts, "worker" : worker, "id" : str(uuid.uuid1())}
            }
        }
    )

    print(result)

def punch_out(log_id, ts):

    result = db.cast.update_one(
        {'logs.id': log_id},
        {
            "$set" : {
                "logs.$.time_out": ts
            }
        }
    )

def get_actives():

    results = []

    cursor = db.cast.aggregate([
        {"$unwind": "$logs"},
        {"$match":{"logs.time_out": {"$exists": False}}},
        {
            "$project": {
                "_id":0,
                "first_name": 1,
                "last_name":1,
                "session":1,
                "time_in": "$logs.time_in",
                "worker": "$logs.worker",
                "log_id": "$logs.id"
            }}
    ])

    for doc in cursor:

        results.append(doc)

    return results
