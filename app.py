from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify
from flask import session as flask_session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from db.models import User, Task, session, Status
from db.schema import Task as TaskSchema


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'
app.secret_key = 'secret_key'
jwt = JWTManager(app)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name', '')
    user_name = data.get('user_name')
    password = data.get('password')

    if not (first_name and user_name and password):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        new_user = User(first_name=first_name, last_name=last_name, user_name=user_name, password=password)
        session.add(new_user)
        session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({'message': 'Username already exists'}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_name = data.get('user_name')
    password = data.get('password')

    user = session.query(User).filter_by(user_name=user_name).first()

    if user and check_password_hash(generate_password_hash(user.password), password):
        access_token = create_access_token(identity=user.id)
        flask_session['access_token'] = access_token
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid user_name or password'}), 401


@app.route('/task', methods=['POST'])
@jwt_required()
def create_task():
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    status = data.get('status', Status.new)
    user_id = get_jwt_identity()

    if not title:
        return jsonify({'message': 'Title is required'}), 400

    new_task = Task(title=title, description=description, status=status, user_id=user_id)
    session.add(new_task)
    session.commit()
    return jsonify({'message': 'Task created successfully'}), 201


@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_all_tasks():
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    offset = (page - 1) * page_size
    tasks = session.query(Task).offset(offset).limit(page_size).all()

    result = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status.value,
            'user_id': task.user_id
        }
        result.append(task_data)

    return jsonify(result), 200


@app.route('/tasks/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_tasks(user_id):
    user = session.get(User, user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    else:
        tasks = session.query(Task).filter_by(user_id=user_id).all()
        tasks_data = [TaskSchema.from_orm(task) for task in tasks]
        tasks_json = [task.dict() for task in tasks_data]
        return jsonify(tasks_json), 200


@app.route('/task/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    task = session.get(Task, task_id)
    if not Task:
        return jsonify({'message': 'Task not found'}), 404
    else:
        task_schema = TaskSchema.from_orm(task)
        return jsonify(task_schema.dict()), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()

    task = session.get(Task, task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    if task.user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        # Check if the provided status is a valid enum value
        if data['status'] not in [status.value for status in Status]:
            return jsonify({'message': 'Invalid status value'}), 400
        else:
            task.status = Status.__call__(data['status'])

    session.commit()
    return jsonify({'message': 'Task updated successfully'}), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = session.get(Task, task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    if task.user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 401
    session.delete(task)
    session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200


@app.before_request
def add_token_to_header():
    if request.endpoint in ('create_task', 'delete_task', 'get_all_tasks', 'get_user_tasks', 'get_task', 'update_task'):
        access_token = flask_session.get('access_token')
        request.environ['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'


if __name__ == '__main__':
    app.run()
