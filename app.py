import json
import os
from functools import reduce

from flask import Flask, url_for, redirect, jsonify, request, abort
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
cors = CORS(app)
userList = [
    {
        'id': 1,
        'name': 'Bob',
        'age': 17
    },
    {
        'id': 2,
        'name': 'Teddy',
        'age': 19
    }
]
comments = [
    {
         "content": "Today is Friday which means there is going to be a little holiday.",
         "time": "2019.03.22"
     },
     {
         "content": "Today is Monday which means there is going to be several hard days.",
         "time": "2019.03.25"
     }
]


@app.route('/')
def root():
    return 'Hello World!'


@app.route('/copy')
def index():
    return redirect(url_for('root'))


@app.route('/user/<username>/info', methods=['GET'])
def get_user_info(username):
    return jsonify(find_user_info(username)), 200


@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['the_file']
    print(f.filename)
    f.save(reduce(os.path.join,[os.path.dirname(__file__), 'files', secure_filename(f.filename)]))
    return jsonify({'code': 200, 'status': 'success'}), 200


@app.route('/user/add', methods=['POST'])
def add_user():
    data = request.get_json()
    if data['name'] == '' or data['age'] is 0:
        abort(400)
    user = {
        'id': userList[-1]['id'] + 1,
        'name':data['name'],
        'age': data['age']
    }
    userList.append(user)
    return wrap_correct_response(userList), 200


@app.route('/comments', methods=['GET'])
def get_comments():
    return wrap_correct_response(read_comments_str()),200


@app.route('/commitComment',methods=['POST'])
def commit_comment():
    data = request.get_json()
    comment = {
        'content': data['content'],
        'time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    comments_str = read_comments_str()
    if comments_str == "":
        comment_list = list()
    else:
        comment_list = json.loads(read_comments_str())
    comment_list.append(comment)
    write_comments_to_file(comment_list)
    return wrap_correct_response(json.dumps(comment))


@app.errorhandler(HTTPException)
def handle_http_error(exc):
    return jsonify({'status': 'error', 'description': exc.description}), exc.code


@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(username)


def find_user_info(username):
    print('user name {}'.format(username))
    print('user list size : ' + str(len(userList)))
    for info in userList:
        if 'name' in info and (info.get('name') == username):
            return info


def read_comments_str():
    file_path = reduce(os.path.join, [os.path.dirname(__file__), 'files', 'comments.json'])
    if os.path.exists(file_path):
        file = open(file_path,'rt')
    else:
        file = open(file_path,'rw')
    content = file.read()
    file.close()
    return content


def write_comments_to_file(list):
    with open(reduce(os.path.join, [os.path.dirname(__file__), 'files', 'comments.json']), 'w') as f:
        f.write(json.dumps(list))
        f.close()


def wrap_correct_response(data):
    response = {
        "status": "success",
        "data": "" if data is None else data
    }
    return jsonify(response)


def wrap_incorrect_response(exception):
    response = {
        "status": "fail",
        "description": "" if exception is None else exception.description
    }
    return jsonify(response)


if __name__ == '__main__':
    fd = open(reduce(os.path.join, [os.path.dirname(__file__), 'files', 'comments.json']),mode='w')
    app.run()

