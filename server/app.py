
#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('_password_hash')
        image = data.get('image_url', '')
        bio = data.get('bio', '')

        if not username or not password:
            return {'error': 'Invalid Details'}, 422

        if User.query.filter_by(username = username).first():
            return {'error': 'Username already exists'}, 400
        
        password_hash = Bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username = username, password = password_hash, image_url = image, bio = bio )
        db.session.add(new_user)
        db.session.commit()

        return {
            'message': 'User created successfully'
        }, 201

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        if user_id:
            user = User.query.get(user_id)
            return {'username' : user.username}, 200
        return {'error': 'Unauthorized, invalid session'}, 401
    

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('_password_hash')

        user = User.query.filter_by(username = username).first()

        if user and Bcrypt.check_password_hash(user.password,password):
            session['user_id'] = user.id
            return{'message': 'Login Succesful'},200
        return{'error': 'incorrect username or password! Try again'},401
class Logout(Resource):
    def delete(self):
        user_id = session.get('user_id')
        
        if not user_id:
            return {'error': 'Unauthorized, no active session'}, 401
        
        session.pop('user_id', None)
        return {'message': 'User has been logged out successfully!'}, 200
    
class RecipeIndex(Resource):
    def get(self):
        pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)