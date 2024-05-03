from flask import Blueprint
from flask_restful import Api
from content.utils.output import output_json

user_bp = Blueprint('user', __name__, url_prefix='/user')
user_api = Api(user_bp)
user_api.representation('application/json')(output_json)

from .user_resource import *
user_api.add_resource(User_Hello, '/hello', endpoint='hello')
user_api.add_resource(User_SMS, '/sms', endpoint='sms')
user_api.add_resource(User_Auth, '/auth', endpoint='auth')
user_api.add_resource(User_Register, '/register', endpoint='register')
user_api.add_resource(User_Login, '/login', endpoint='login')
user_api.add_resource(Phone_Exist, '/isExist', endpoint='isExist')
user_api.add_resource(User_Logout, '/logout', endpoint='logout')
