from flask import Blueprint, request
from App.extension import db
from App.common.common_response import CommonResponse
from flask_login import current_user
from App.models.shopping_cart_model import ShoppingCart, db_shopping_cart_foods
from App.models.shopping_DTO import ShoppingDTO
from flask import jsonify
from App.models.food_model import FoodModel

shopping_cart_view = Blueprint('shopping_cart', __name__)


@shopping_cart_view.route("/shoppingCart/select", methods=['GET'])
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


@shopping_cart_view.route("/shoppingCart/delete", methods=['POST'])
def delete_item_on_shopping_cart():
    cart = ShoppingCart.query.filter_by(user_id=current_user.id).first()

    if not cart:
        return jsonify(CommonResponse.failure("could not find cart")), 404

    food_id_to_delete = request.json.get('foodId')

    if not food_id_to_delete:
        return jsonify(CommonResponse.failure("required food id")), 400

    food_to_delete = FoodModel.query.get(food_id_to_delete)

    if not food_to_delete:
        return jsonify(CommonResponse.failure("Could not find the food")), 404

    try:
        # 从购物车中移除食物
        cart.foods.remove(food_to_delete)
        db.session.commit()
        return jsonify(CommonResponse.success("delete successful")), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(CommonResponse.failure(message=str(e))), 500


@shopping_cart_view.route("/shoppingCart/add", methods=['POST'])
def add_item_to_shopping_cart():

    cart = ShoppingCart.query.filter_by(user_id=current_user.id).first()

    if not cart:
        return jsonify(CommonResponse.failure("Could not find cart")), 404

    food_id_to_add = request.json.get('foodId')

    if not food_id_to_add:
        return jsonify(CommonResponse.failure("Required food ID")), 400

    food_to_add = FoodModel.query.get(food_id_to_add)

    if not food_to_add:
        return jsonify(CommonResponse.failure("Could not find the food")), 404

    try:
        # 添加食物到购物车
        cart.foods.append(food_to_add)
        db.session.commit()
        return jsonify(CommonResponse.success("Item added to cart")), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(CommonResponse.failure(message=str(e))), 500
