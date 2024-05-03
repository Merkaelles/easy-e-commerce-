from flask_script import Manager  # flask_script 可使用命令调用视图函数，从而使flask与web分离
from shop import create_app
from content.model import db

app = create_app('develop')
manager = Manager(app)


@manager.command
def hello():
    print('hello, I am flask_script')


with app.app_context():
    class User(db.Model):
        __tablename__ = 'test_user'
        id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
        username = db.Column(db.String(255), doc='用户名')
        password = db.Column(db.String(255), doc='密码')


    db.create_all()


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_user(username, password):
    u = User(username=username, password=password)
    db.session.add(u)
    db.session.commit()
    print('create a user by command')


if __name__ == '__main__':
    manager.run()
