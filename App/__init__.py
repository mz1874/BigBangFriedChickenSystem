from flask import Flask
from App.extension import init_extension
from App.extension import login_manager
from App.controllers.index_view import home_view
from App.models.user_model import UserModel
from App.models.role_model import RoleModel
from App.models.feedback_model import FeedbackModel
from App.controllers.user_view import user_view
from App.controllers.feedback_view import feedback_view
from App.models.authorization import AuthorizationModel
from App.models.food_model import FoodModel
from App.models.food_category_model import FoodCategory
from App.controllers.food_category_view import food_category_view
from App.controllers.shopping_cart import shopping_cart_view
from App.controllers.food_view import food_view
from App.models.order_model import OrderModel
from App.models.shopping_cart_model import ShoppingCart
from App.controllers.order_view import order_view
from App.config import config
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(food_category_view)
    app.register_blueprint(feedback_view)
    app.register_blueprint(home_view)
    app.register_blueprint(shopping_cart_view)
    app.register_blueprint(order_view)
    app.register_blueprint(user_view)
    app.register_blueprint(food_view)

    login_manager.init_app(app)
    init_extension(app)
    return app
