import json
import random
from flask import current_app, request, g
from flask_restful import Resource, reqparse
from content.model import db
from content.model.user import User
from content.utils import const
# from content.utils.decorators import login_required
from content.utils.sms import send_sms
from content.utils.limiter import limiter
from content.utils.shop_redis import redis_client
from content.utils.parser import mobile, email_addr, regex
from content.utils.token_pyjwt import generate_tokens, verify_tokens
from flask_limiter.util import get_remote_address


class User_Hello(Resource):
    # method_decorators = {  # 测试单独在class给方法添加装饰器, 若定义了before_request钩子， 则不必用装饰器了
    #     'get': [login_required],
    #     'post': [login_required],
    # }

    def get(self):
        u = User.query.all()
        for i in u:
            print(i)
        return {'msg': 'Hi, Everyone'}


class User_SMS(Resource):
    error_message = '请求验证码过于频繁'
    decorators = [
        limiter.limit(const.LIMIT_SMS_CODE_BY_PHONE, key_func=lambda: request.args['phone'],
                      error_message=error_message),  # 限流手机号
        limiter.limit(const.LIMIT_SMS_CODE_BY_IP, key_func=get_remote_address, error_message=error_message)  # 限流ip
    ]

    def get(self):
        phone = request.args.get('phone').strip()
        code = random.randint(100000, 999999)
        result = send_sms(phone, code)
        result = json.loads(result)  # json.loads()可将json变成字典
        if result['Message'] != 'OK':
            print(result)
        else:
            result['phone'] = phone
            redis_client.setex("shopping-verifycode:{}".format(phone), const.SMS_VERIFY_CODE_EXPIRE, code)
            return result


class User_Auth(Resource):
    def post(self):
        rp = reqparse.RequestParser()
        rp.add_argument('phone', type=mobile, required=True, location='args')
        rp.add_argument('code', type=regex(r'^\d{6}$'), required=True, location='args')
        args = rp.parse_args()
        phone = args.phone
        code = args.code

        try:
            verify_code = redis_client.get(f'shopping-verifycode:{phone}')
        except ConnectionError as e:
            current_app.logger.error(e)
            return {'message': 'redis db connection failed'}, 400

        if not verify_code or verify_code.decode() != code:
            return {'message': 'Invalid code'}, 400
        return {'phone': phone, 'msg': 'verify_successfully'}


class User_Register(Resource):
    def post(self):
        rp = reqparse.RequestParser()
        rp.add_argument('username', required=True, location='form')
        rp.add_argument('password', required=True, location='form')
        rp.add_argument('phone', type=mobile, required=True, location='form')
        rp.add_argument('email', type=email_addr, location='form')
        args = rp.parse_args()
        username = args.username
        password = args.password
        phone = args.phone
        email = args.email

        u = User.query.filter(User.username == username).first()
        if u:
            current_app.logger.info('This username already exists')
            return {'message': 'This username already exists, please change others'}, 400

        u = User(username=username, pwd=password, phone=phone, email=email)  # password在模型里加密后用加密的方法名代替变量
        db.session.add(u)
        db.session.commit()
        return {'msg': 'register successfully'}


class User_Login(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            return {'message': 'missing information'}, 402
        user = User.query.filter(User.username == username).first()
        if user:
            if user.check_password(password):
                token = generate_tokens(user.id)
                return {'msg': 'Login Successfully', 'token': token, 'username': username}
        return {'message': 'wrong username or password'}, 400


class User_Logout(Resource):
    def post(self):
        if g.user_id:
            g.user_id = None
        return {'msg': '退出登录'}


class Phone_Exist(Resource):
    def post(self):
        phone = request.form.get('phone')
        u = User.query.filter(User.phone == phone).first()
        if u:
            return {'isExist': True, 'message': '该手机号已经注册'}, 203
        return {'msg': '手机号可以注册'}
