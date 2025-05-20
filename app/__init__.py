from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt = JWTManager(app)

    from app.routes import user_routes, project_routes, task_routes, masterUser_routes
    app.register_blueprint(user_routes.user)
    app.register_blueprint(project_routes.projectBp)
    app.register_blueprint(task_routes.taskBp)
    app.register_blueprint(masterUser_routes.masterUser)

    return app