from flask_script import Manager  # flask_script 可使用命令调用视图函数，从而使flask与web分离
from flask_migrate import Migrate, MigrateCommand
from shop import create_app
from content.model import db

app = create_app('develop')
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
