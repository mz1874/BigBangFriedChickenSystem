from flask import Flask
from App.extension import init_extension
from App.extension import login_manager
from App.controllers.index_view import home_view
from App.models.user_model import UserModel
from App.models.role_model import RoleModel
from App.controllers.user_view import user_view
from App.models.authorization import AuthorizationModel
from App.models.food_model import FoodModel
from App.models.food_category_model import FoodCategory
from App.controllers.food_category_view import food_category_view
from App.controllers.shopping_cart import shopping_cart_view
from App.controllers.food_view import food_view
from App.models.order_model import OrderModel
from App.models.shopping_cart_model import ShoppingCart
from App.controllers.order_view import order_view
def create_app():
    app = Flask(__name__)
    # 不要使用这个
    db_url = "mysql+pymysql://root:v6%+nT8M@192.168.0.60:3306/online_ordering_system?charset=utf8mb4"
    # 打开注释，使用服务器配置进行数据同步
    # db_url = "mysql+pymysql://root:v6%+nT8McT7zvn%@bugcreator.org.cn:3306/online_ordering_system?charset=utf8mb4"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "v6%+nT8McT7z"
    app.register_blueprint(food_category_view)
    app.register_blueprint(home_view)
    app.register_blueprint(shopping_cart_view)
    app.register_blueprint(order_view)
    app.register_blueprint(user_view)
    login_manager.init_app(app)
    init_extension(app)
    return app
