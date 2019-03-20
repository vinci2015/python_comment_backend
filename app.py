from flask import Flask, url_for, redirect, jsonify, request, abort
import os
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

app = Flask(__name__)
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
    f.save(reduce(os.path.join,[os.path.dirname(__file__),'files',secure_filename(f.filename)]))
    return jsonify({ 'code':200,'status':'success'}), 200

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
    return jsonify(userList), 200


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


if __name__ == '__main__':
    app.run()
