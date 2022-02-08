from flask import request
from flask_restx import Resource, Api, Namespace, fields
import jwt
import bcrypt

users = {}

Auth = Namespace(
    name='Auth',
    description='로그인을 위한 api',
)

user_fields = Auth.model('User', {
    'name': fields.String(description='a User Name', required=True, example="kimsh4265")
})

user_fields_auth = Auth.inherit('User Auth', user_fields, {
    'password': fields.String(description='Password', required = True, example='password')
})

jwt_fields = Auth.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must include in header', required= True, example='edy353jsif~~~~~')
})

@Auth.route('/register')
class AuthRegister(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={500: 'Register Failed'})
    def post(self):
        name = request.json.get('name')
        password = request.json.get('password')
        if name in users:
            return{
                'message': 'Register Failed'
            }, 500
        else:
            users[name] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            return {
                'Autorization': jwt.encode({'name': name}, "secret", algorithm='HS256')
            }, 200

@Auth.route('/login')
class AuthLogin(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={404: 'User Not Found'})
    @Auth.doc(responses={500: 'Auth Failed'})
    def post(self):
        name = request.json.get('name')
        password = request.json.get('password')
        if name not in users:
            return {
                'message': 'User Not Found'
            }, 404
        elif not bcrypt.checkpw(password.encode('utf-8'), users[name]):
            return {
                'message': 'Auth Failed'
            }, 500
        else:
            return {
                'Authorization': jwt.encode({'name': name}, "secret", algorithm='HS256')
            }, 200

@Auth.route('/get')
class AuthGet(Resource):
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={500: 'Login Failed'})
    def get(self):
        header = request.headers.get('Authorization')
        if header == None:
            return {
                'message': 'Please Login'
            }, 404
        else:
            data = jwt.decode(header, "secret", algorithms='HS256')
            return data, 200