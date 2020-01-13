import os
from flask_migrate import Migrate
from app.views import create_app
from shared import db

app = create_app(os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
if __name__ == '__main__':
    app.run()