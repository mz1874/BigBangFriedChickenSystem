from flask import Blueprint, request
from sqlalchemy import select, update, func

from App.extension import db
from App.common.common_response import CommonResponse
from flask_login import current_user
from App.models.shopping_cart_model import ShoppingCart
from App.models.shopping_DTO import ShoppingDTO
from flask import jsonify
from App.models.food_model import FoodModel
from App.models.shopping_cart_model import db_shopping_cart_foods
from datetime import datetime


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
    cart = ShoppingCart.query.filter_by(user_id=request.json.get("currentUserId")).first()

    if not cart:
        return jsonify(CommonResponse.failure("Could not find cart")), 404

    food_id_to_add = request.json.get('foodId')
    quality = request.json.get('quality', 1)  # 默认质量为1

    if not food_id_to_add:
        return jsonify(CommonResponse.failure("Required food ID")), 400

    food_to_add = FoodModel.query.get(food_id_to_add)

    if not food_to_add:
        return jsonify(CommonResponse.failure("Could not find the food")), 404

    # 检查是否已经存在于购物车中
    stmt = select(db_shopping_cart_foods).where(
        db_shopping_cart_foods.c.shopping_cart_id == cart.id,
        db_shopping_cart_foods.c.food_id == food_to_add.id
    )
    result = db.session.execute(stmt).fetchone()

    if result:
        # 确保 result.quality 是整数
        current_quality = result.quality or 0
        # 更新现有记录的数量
        update_stmt = (
            update(db_shopping_cart_foods).
            where(
                db_shopping_cart_foods.c.shopping_cart_id == cart.id,
                db_shopping_cart_foods.c.food_id == food_to_add.id
            ).
            values(quality=current_quality + quality)
        )
        try:
            db.session.execute(update_stmt)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(CommonResponse.failure(message=str(e))), 500
    else:
        # 添加新记录
        new_record = {
            'shopping_cart_id': cart.id,
            'food_id': food_to_add.id,
            'quality': quality,
            'created_at': datetime.utcnow()
        }
        try:
            insert_stmt = db_shopping_cart_foods.insert().values(**new_record)
            db.session.execute(insert_stmt)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(CommonResponse.failure(message=str(e))), 500

    # 计算总价
    total_price_stmt = db.session.query(
        func.sum(FoodModel.price * db_shopping_cart_foods.c.quality)
    ).join(
        db_shopping_cart_foods, FoodModel.id == db_shopping_cart_foods.c.food_id
    ).filter(
        db_shopping_cart_foods.c.shopping_cart_id == cart.id
    )

    total_price = db.session.execute(total_price_stmt).scalar()

    return jsonify(CommonResponse.success("Item added/updated in cart", data={"total_price": total_price})), 200