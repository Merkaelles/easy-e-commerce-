from itsdangerous import TimedJSONWebSignatureSerializer   # itsdangerous version == 2.0.1
import const
from flask import current_app
from content.model.user import User


def generate_tokens(uid):
    serializer = TimedJSONWebSignatureSerializer(secret_key=const.SECRET_KEY, expires_in=const.JWT_EXPIRY_SECOND)
    return serializer.dumps({'id': uid}).decode()


def verify_tokens(token):
    serializer = TimedJSONWebSignatureSerializer(secret_key=const.SECRET_KEY, expires_in=const.JWT_EXPIRY_SECOND)
    try:
        data = serializer.loads(token)
    except Exception as e:
        current_app.logger.info(e)
        return {'message': 'token 验证失败'}
    u = User.query.filter(User.id == data['id']).first()
    if u and u.login_status != 0:
        return {'message': '用户登录已过期'}
    return {'id': u.id}

