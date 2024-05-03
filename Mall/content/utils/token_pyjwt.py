import jwt
from jwt import PyJWTError

from . import const
from flask import current_app
from content.model.user import User
from datetime import datetime, timedelta


def generate_tokens(uid):
    payload = {
        'id': uid,
        'exp': datetime.utcnow() + timedelta(seconds=const.JWT_EXPIRY_SECOND)  # exp must be 格林尼治时间格式
    }
    token = jwt.encode(payload, key=const.SECRET_KEY, algorithm='HS256')
    return token


def verify_tokens(token):
    try:
        data = jwt.decode(token, key=const.SECRET_KEY, algorithms='HS256')
    except PyJWTError as e:
        current_app.logger.info(e)
        return {'message': 'token 验证失败'}
    u = User.query.filter(User.id == data['id']).first()
    if u and u.login_status != 0:
        return {'message': '用户登录已过期'}
    return {'id': u.id}
