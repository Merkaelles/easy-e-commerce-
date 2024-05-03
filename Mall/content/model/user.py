from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), doc='用户名')
    password = db.Column(db.String(255), doc='密码')
    phone = db.Column(db.String(11), doc='电话')
    email = db.Column(db.String(255), doc='邮箱')
    nick_name = db.Column(db.String(255), doc='昵称')
    remark = db.Column(db.String(255), doc='备注')
    icon = db.Column(db.String(255), doc='头像')

    login_time = db.Column(db.DateTime, default=datetime.now(), doc='登陆时间')
    login_status = db.Column(db.Integer, doc='登录状态', default=0)
    create_time = db.Column(db.DateTime, default=datetime.now(), doc='注册时间')
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), doc='修改时间')

    @property  # @property将所装饰的方法包装成属性，以属性的形式被调用和访问
    def pwd(self):
        return self.password

    @pwd.setter
    def pwd(self, x_password):
        self.password = generate_password_hash(x_password)

    def check_password(self, x_password):
        return check_password_hash(self.password, x_password)

    def __str__(self):
        return f'{self.username}-{self.remark}'
