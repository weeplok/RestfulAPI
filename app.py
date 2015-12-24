#!flask/bin/python
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return "Flask Running.."


tasks = [
    {
        'id': 1101,
        'title': 'buy me the none',
        'description': 'mike like cheese',
        'done': False
    }
]


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        # abort(400)
        return "abort(400)"
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v1.0/tasks/upload', methods=['POST'])
def jdata_push():

    import pymongo

    connection = pymongo.MongoClient('localhost', 27017)
    db = connection.Table_RemoteSet
    collection = db.users
    if not request.json:
        return "find no json, abort(400)."

    collection.insert(request.json)

    for data in collection.find():
        print data

    return "remote data upload successfully.."


@app.route('/todo/api/v1.0/tasks/download', methods=['GET'])
def jdata_pop():

    import pymongo

    connection = pymongo.MongoClient('localhost', 27017)
    db = connection.Table_RemoteSet
    collection = db.users

    ans = 'Total Collection CountNumber is ' + str(collection.find().count()) + '\n'
    print 'echo ans done..'

    return ans


if __name__ == '__main__':
    app.run('172.16.42.7', debug=True)
