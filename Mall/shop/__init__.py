from flask import Flask
from settings import config_map
from content.model.goods import *


def create_app(config_type):
    app = Flask(__name__)
    app.config.from_object(config_map.get(config_type))  # 1.配置

    from content.utils.loggings import create_logger  # 2.日志
    create_logger(app)

    from content.model import db  # 3.数据库
    db.init_app(app)

    from content.utils.limiter import limiter  # 4.限流器
    limiter.init_app(app)

    from content.utils.shop_redis import redis_client  # 5.redis缓存
    redis_client.init_app(app)

    from content.utils.request_hook import jwt_request_auth  # 6.添加请求钩子, 用户所有操作都经过钩子验证
    app.before_request(jwt_request_auth)

    from .resource.user import user_bp  # 7.蓝图
    from .resource.category import category_bp
    from .resource.goods import goods_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(goods_bp)

    return app
