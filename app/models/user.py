import hashlib
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='assignee', lazy=True)


class MasterUser(db.Model):
    __tablename__ = 'master_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, raw_password):
        self.password = hashlib.md5(raw_password.encode('utf-8')).hexdigest()

    def check_password(self, raw_password):
        return self.password == hashlib.md5(raw_password.encode('utf-8')).hexdigest()