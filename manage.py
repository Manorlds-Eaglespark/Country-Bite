import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.views import db, create_app
from app.models.users import User
from app.models.posts import Post
from app.models.likes import Like
from app.models.bookmarks import Bookmark
from app.models.images import PhotoImage
from app.models.feedback import Feedback

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
