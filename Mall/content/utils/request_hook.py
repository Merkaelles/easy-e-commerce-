from flask import g, request, current_app
from .token_pyjwt import verify_tokens


def jwt_request_auth():
    g.user_id = None
    try:
        token = request.headers.get('token')
    except Exception as e:
        current_app.logger.info('headers中没有token')
        return
    if token is not None:                    # 登陆前不会产生token, 故不需要验证token
        result = verify_tokens(token)
        if 'id' in result:
            g.user_id = result['id']
