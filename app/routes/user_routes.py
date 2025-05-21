from app.models.task import Task
from app.utils.helper import UtilsHelper
from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
import re

user = Blueprint('users', __name__, url_prefix='/users')

@user.route('/', methods=['POST'])
@jwt_required()
def create_user():
    """
    function Create a new user
    """
    try:
        data = request.json
        requiredError = UtilsHelper().check_required_fields(
            data, 
            ['name', 'email']
        )
        if requiredError:
            return requiredError, 400
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get('email', '')):
            return {"error": "Invalid email format"}, 400
        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "Email already exists"}, 400
        return jsonify({
            "message": "User added succesfully", "data": {"id": user.id, "name": user.name, "email": user.email}}), 201
    except Exception as e:
        return {"error": str(e)}, 500

@user.route('/', methods=['GET'])
@jwt_required()
def list_users():
    """
    function List all users
    """
    users = User.query.order_by(User.id.desc()).all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

@user.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    function Get a user by ID
    """
    user = User.query.get(user_id)
    if not user:
        return UtilsHelper().error_msg_of_data('user'), 404
    return jsonify({"id": user.id, "name": user.name, "email": user.email})

@user.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    function Delete a user by ID"""
    user = User.query.get(user_id)
    if not user:
        return UtilsHelper().error_msg_of_data('user'), 404
    tasks = Task.query.filter_by(user_id=user_id).all()
    if any(dep.status != 'completed' for dep in tasks.dependencies):
            return {"error": "All dependencies must be completed first"}, 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
