from flask import Blueprint, jsonify, request, session
from App.common.decorators import requires_permission
from App.extension import db
from App.common.common_response import CommonResponse
from App.models.user_model import UserModel
from App.models.role_model import RoleModel
from App.models.food_category_model import FoodCategory
from flask_login import current_user
from sqlalchemy import func
from App.models.shopping_cart_model import ShoppingCart, db_shopping_cart_foods
from App.models.shopping_DTO import ShoppingDTO

shopping_cart_view = Blueprint('shopping_cart', __name__)

from flask import jsonify
from sqlalchemy import func


@shopping_cart_view.route("/shopping_cart", methods=['GET'])
def show_shopping_cart():
    user = current_user
    cart = ShoppingCart.query.filter_by(user_id=user.id).first()
    foods = cart.foods.order_by(db_shopping_cart_foods.c.created_at.desc()).all()
    shopping_dto_list = []
    # 使用聚合函数获取每个食物的数量
    temp_table = (db.session.query(db_shopping_cart_foods.c.food_id,
                                   db_shopping_cart_foods.c.quality,
                                   db_shopping_cart_foods.c.created_at)
                  .filter_by(shopping_cart_id=cart.id).group_by(
        db_shopping_cart_foods.c.food_id).all())
    for food in foods:
        for q in temp_table:
            if food.id == q.food_id:
                dto = ShoppingDTO(
                    food.id,
                    q.quality,
                    food.price,
                    food.food_name,
                    food.img,
                    added_time=q.created_at,
                )
                shopping_dto_list.append(dto.__dict__)  # Convert ShoppingDTO object to dictionary

    # Return the list of dictionaries directly
    return jsonify(CommonResponse.success(shopping_dto_list))