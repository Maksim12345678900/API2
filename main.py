
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Предполагаемая структура данных
users = {}
posts = {}
next_user_id = 1
next_post_id = 1

@app.route('/users', methods=['POST'])
def create_user():
    global next_user_id
    if not request.json or 'username' not in request.json or 'email' not in request.json:
        abort(400)  # Некорректные данные

    user = {
        'id': next_user_id,
        'username': request.json['username'],
        'email': request.json['email']
    }
    users[next_user_id] = user
    next_user_id += 1
    return jsonify({'user': user}), 201

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_operations(user_id):
    if user_id not in users:
        abort(404)  # Пользователь не найден

    if request.method == 'GET':
        return jsonify({'user': users[user_id]})

    if request.method == 'PUT':
        if not request.json:
            abort(400)  # Некорректные данные
        user = users[user_id]
        user['username'] = request.json.get('username', user['username'])
        user['email'] = request.json.get('email', user['email'])
        return jsonify({'user': user})

    if request.method == 'DELETE':
        del users[user_id]
        return '', 204

@app.route('/posts', methods=['POST'])
def create_post():
    global next_post_id
    if not request.json or 'title' not in request.json or 'content' not in request.json or 'user_id' not in request.json:
        abort(400)  # Некорректные данные
    if request.json['user_id'] not in users:
        abort(404)  # Пользователь не найден

    post = {
        'id': next_post_id,
        'title': request.json['title'],
        'content': request.json['content'],
        'user_id': request.json['user_id']
    }
    posts[next_post_id] = post
    next_post_id += 1
    return jsonify({'post': post}), 201

@app.route('/posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def post_operations(post_id):
    if post_id not in posts:
        abort(404)  # Пост не найден

    if request.method == 'GET':
        return jsonify({'post': posts[post_id]})

    if request.method == 'PUT':
        if not request.json:
            abort(400)  # Некорректные данные
        post = posts[post_id]
        post['title'] = request.json.get('title', post['title'])
        post['content'] = request.json.get('content', post['content'])
        return jsonify({'post': post})

    if request.method == 'DELETE':
        del posts[post_id]
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
