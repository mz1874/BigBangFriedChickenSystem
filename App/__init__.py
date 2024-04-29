from flask import Flask
from App.extension import init_extension
from App.controllers.index_view import home_view
from App.models.UserModel import UserModel
from App.models.RoleModel import RoleModel
from App.controllers.user_view import user_view


def create_app():
    app = Flask(__name__)
    # 不要使用这个
    db_url = "mysql+pymysql://root:v6%+nT8M@pi4.com:3306/online_ordering_system?charset=utf8mb4"
    # 打开注释，使用服务器配置进行数据同步
    # db_url = "mysql+pymysql://root:v6%+nT8M@bugcreator.org.cn:3306/online_ordering_system?charset=utf8mb4"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.register_blueprint(home_view)
    app.register_blueprint(user_view)
    init_extension(app)
    return app
