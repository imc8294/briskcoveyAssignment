from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task
from app.models.user import User
from app.models.project import Project
from sqlalchemy.orm import joinedload
from app.utils.helper import UtilsHelper
from flask_jwt_extended import jwt_required

taskBp = Blueprint('tasks', __name__, url_prefix='/tasks')

@taskBp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    """
    function for Create a new task.
    """
    data = request.json
    requiredError = UtilsHelper().check_required_fields(
        data, 
        ['title', 'project_id', 'status', 'user_id']
    )
    if requiredError:
        return requiredError, 400
    statusError = UtilsHelper().check_status_value(
        data.get('status', 'pending'),
        ['pending', 'in_progress']
    )
    if statusError:
        return statusError, 400
    project = Project.query.get(data['project_id'])
    if not project:
        return UtilsHelper().error_msg_of_data('project'), 404
    user = User.query.get(data['user_id'])
    if not user:
        return UtilsHelper().error_msg_of_data('user'), 404
    task = Task(
        title=data['title'],
        status=data.get('status', 'pending'),
        user_id=user.id, 
        project_id=project.id
    )
    db.session.add(task)
    db.session.flush()

    if 'dependencies' in data:
        for dep_id in data['dependencies']:
            dep = Task.query.get(dep_id)
            if dep:
                if check_circular_dependency(task, dep):
                    db.session.rollback()
                    return {"error": "Circular dependency detected"}, 400
                task.dependencies.append(dep)

    db.session.commit()
    return jsonify({"id": task.id, "title": task.title}), 201

@taskBp.route('/', methods=['GET'])
@jwt_required()
def list_task():
    """
    function for List all tasks.
    """
    task = Task.query.options(joinedload(Task.dependencies)).all()
    return jsonify([{
        "id": t.id, 
        "name": t.title,
        "status": t.status,
        "dependencies": [dep.id for dep in t.dependencies]
    } for t in task])
    

@taskBp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """
    function for Get a task by ID.
    """
    task = Task.query.options(joinedload(Task.dependencies)).get(task_id)
    if not task:
        return UtilsHelper().error_msg_of_data('task'), 404
    return jsonify({
        "id": task.id,
        "title": task.title,
        "status": task.status,
        "dependencies": [t.id for t in task.dependencies]
    })

@taskBp.route('/update_status/<int:task_id>', methods=['POST'])
@jwt_required()
def update_task_status(task_id):
    """
    function for Update a task status by ID.
    """
    try:
        data = request.json
        requiredError = UtilsHelper().check_required_fields(
            data, ['status']
        )
        if requiredError:
            return requiredError, 400
        task = Task.query.options(joinedload(Task.dependencies)).get(task_id)
        if not task:
            return UtilsHelper().error_msg_of_data('task'), 404

        if 'status' in data:
            statusError = UtilsHelper().check_status_value(
            data.get('status', 'pending'),
            ['pending', 'in_progress', 'completed']
        )
            if statusError:
                return statusError, 400
            if data['status'] == 'completed':
                if any(dep.status != 'completed' for dep in task.dependencies):
                    return {"error": "All dependencies must be completed first"}, 400
            task.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Task Status updated succesfully'}), 200
    except Exception as e:
        return {"error": str(e)}, 500
    

@taskBp.route('/update_dependency/<int:task_id>', methods=['POST'])
@jwt_required()
def update_task_dependency(task_id):
    """
    function for Update dependency status by ID.
    """
    
    try:
        data = request.json
        requiredError = UtilsHelper().check_required_fields(
            data, ['dependencies']
        )
        if requiredError:
            return requiredError, 400
        task = Task.query.options(joinedload(Task.dependencies)).get(task_id)
        if not task:
            return UtilsHelper().error_msg_of_data('task'), 404
        task.dependencies.clear()
        for dep_id in data['dependencies']:
            dep = Task.query.get(dep_id)
            if dep:
                if check_circular_dependency(task, dep):
                    db.session.rollback()
                    return {"error": "Circular dependency detected"}, 400
                task.dependencies.append(dep)
        db.session.commit()
        return jsonify({'message': 'Dependency updated succesfully'}), 200
    except Exception as e:
        return {"error": str(e)}, 500

@taskBp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def list_user_tasks(user_id):
    """
    function for List all tasks for a specific user.
    """
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{ "id": t.id, "title": t.title, "status": t.status } for t in tasks])

@taskBp.route('/status/<string:status>', methods=['GET'])
@jwt_required()
def list_tasks_by_status(status):
    """
    function for List all tasks by status.
    """
    statusError = UtilsHelper().check_status_value(
        status, ['pending', 'in_progress', 'completed']
    )
    if statusError:
        return statusError, 400
    tasks = Task.query.filter_by(status=status).all()
    return jsonify([{ "id": t.id, "title": t.title } for t in tasks])


def check_circular_dependency(task, dependency):
    """
    function for Check circular dependencies between tasks.
    """
    def has_path_to(target, current):
        if current == target:
            return True
        return any(has_path_to(target, dep) for dep in current.dependencies)

    return has_path_to(task, dependency)
