""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re
from flask.ext.bcrypt import Bcrypt

bcrypt = Bcrypt()

class Registration(Model):
    def __init__(self):
        super(Registration, self).__init__()

    def register_user(self, user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        errors = []
        
        if not user['first_name']:
            errors.append('First name cannot be blank')
        if len(user['first_name']) < 2:
            errors.append("First name must be at least 2 characters long")
        if not user['first_name'].isalpha():
            errors.append("First name must only contain letters")
        if not user['last_name']:
            errors.append('Last name cannot be blank')
        if len(user['last_name']) < 2:
            errors.append("Last name must be at least 2 characters long")
        if not user['last_name'].isalpha():
            errors.append("Last name must only contain letters")
        if not user['email']:
            errors.append('Email cannot be blank')
        if not EMAIL_REGEX.match(user['email']):
            errors.append("Invalid Email Address!")
        if not user['password']:
            errors.append('Password cannot be blank')
        if len(user['password']) < 8:
            errors.append("Password must be at least 8 characters.")
        if user['password'] != user['confirm_pw']:
            errors.append("Password and confirmation do not match.")    
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = user['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
            data = {
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email'],
            'password': hashed_pw
            }
            self.db.query_db(query, data)
            return {"status": True}

    def login_validation(self, user):
        password = user['password']
        query = "SELECT * FROM users WHERE email = :temp_email"
        data = {'temp_email': user['email']}
        user = self.db.query_db(query, data)
        if not user:
            return False
        else:
            if self.bcrypt.check_password_hash(user[0]['password'], password):
                    return user
            else:
                return False

        
    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """