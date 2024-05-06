from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_cors import CORS
from flask_login import LoginManager
db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'simple'})


def init_extension(app):
    CORS(app)
    db.init_app(app=app)
    cache.init_app(app=app)
    migrate.init_app(app=app, db=db)
