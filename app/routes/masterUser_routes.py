from app.utils.helper import UtilsHelper
from flask import Blueprint, request, jsonify
from app import db
from app.models.project import Project
from app.models.user import MasterUser
from flask_jwt_extended import create_access_token

masterUser = Blueprint('masterUser', __name__, url_prefix='/masterlogin')

@masterUser.route('/', methods=['POST'])
def login():
    try:
        data = request.json
        requiredError = UtilsHelper().check_required_fields(
            data, 
            ['email', 'password']
        )
        if requiredError:
            return requiredError, 400
        userdata = MasterUser.query.filter_by(email=data['email']).first()
        print(userdata)
        if not userdata: 
            return jsonify({"message": "User not found"}), 404
        elif not userdata.check_password(data['password']):
            return jsonify({"message": "Invalid password"}), 401
        access_token = create_access_token(identity=userdata.email)
        return jsonify(access_token=access_token)
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    return jsonify({"id": project.id, "name": project.name}), 201