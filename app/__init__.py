import os
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from settings import Config


db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name='管理系统', template_mode='bootstrap3')
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
bootstrap = Bootstrap()
moment = Moment()


def create_app(FLASK_CONFIG=Config):

    app = Flask(__name__)
    app.config.from_object(FLASK_CONFIG)

    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    try:
        app.config['AVATAR_FOLDER'] = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'])
        os.makedirs(app.config['AVATAR_FOLDER'])
    except OSError:
        pass
    # admin views
    from .models import User
    from .models import DoctorCode
    from app.utils import UserModelView
    from app.utils import DoctorCodeModelView
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(DoctorCodeModelView(DoctorCode, db.session))

    from app.errors import errors_bp
    app.register_blueprint(errors_bp, url_prefix='/error')

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # from app.admin import admin_bp
    # app.register_blueprint(admin_bp)

    from app.main import main_bp
    app.register_blueprint(main_bp)




    return app


from app import models