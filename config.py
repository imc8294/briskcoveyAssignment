import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:123456@localhost/briskcoveyAssignment')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'Qwerty1234')  
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Token expiration time in seconds (1 hour)
