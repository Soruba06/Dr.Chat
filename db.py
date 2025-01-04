from flask_pymongo import PyMongo

mongo = PyMongo()

def init_app(app):
    mongo.init_app(app)

def insert_user(username, password, email):
    mongo.db.users.insert_one({'username': username, 'password': password, 'email': email})

def find_user(username):
    return mongo.db.users.find_one({'username': username})

def get_user_email(username):
    user = find_user(username)
    return user['email'] if user else None
