from app.utils.helper import UtilsHelper
from flask import Blueprint, request, jsonify
from app import db
from app.models.project import Project
from app.models.task import Task
from flask_jwt_extended import jwt_required

projectBp = Blueprint('projects', __name__, url_prefix='/projects')

@projectBp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    data = request.json
    requiredError = UtilsHelper().check_required_fields(
        data, 
        ['name', 'description']
    )
    if requiredError:
        return requiredError, 400
    project = Project(name=data['name'], description=data.get('description'))
    db.session.add(project)
    db.session.commit()
    return jsonify({"id": project.id, "name": project.name}), 201

@projectBp.route('/', methods=['GET'])
@jwt_required()
def list_projects():
    projects = Project.query.order_by(Project.id.desc()).all()
    return jsonify([{"id": p.id, "name": p.name} for p in projects])

@projectBp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return UtilsHelper().error_msg_of_data('Project'), 404
    return jsonify({"id": project.id, "name": project.name, "description": project.description})

@projectBp.route('/<int:project_id>/tasks', methods=['GET'])
@jwt_required()
def list_project_tasks(project_id):
    
    tasks = Task.query.filter_by(project_id=project_id).all()
    return jsonify([{ "id": task.id, "title": task.title, "status": task.status } for task in tasks])
