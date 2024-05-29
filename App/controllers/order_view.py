from select import select

from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime
from App.common.common_response import CommonResponse
from App.models.food_model import FoodModel
from App.models.user_model import UserModel
from App.models.order_model import OrderModel
from App.extension import db
from App.models.shopping_cart_model import db_shopping_cart_foods
from App.models.order_model import db_order_foods

order_view = Blueprint('order_view', __name__)


@order_view.route("/order/selectOrderByUserId", methods=["GET"])
def selectOrder():
    userId = request.args.get("userId")
    user = UserModel.query.filter_by(id=userId).first()
    if user is not None:
        orders = user.orders
        if orders is not None:
            result = [{"id": order.id, "orderTime": order.order_time, "total": order.total, "status": order.status} for
                      order in orders]
            return jsonify(CommonResponse.success(result))
        else:
            return jsonify(CommonResponse.success())
    else:
        CommonResponse.failure("User not found")


@order_view.route("/order/selectFoodByOrderId", methods=["GET"])
def select_food_by_order_id():
    order_id = request.args.get("orderId")
    if order_id is None:
        return CommonResponse.failure("orderId is required")

    # 查询订单
    order = OrderModel.query.filter_by(id=order_id).first()
    if order is None:
        return CommonResponse.failure("orderId is invalid")

    # 查询订单下的食物
    foods = order.order_foods

    # 查询订单中的食物数量
    items = db.session.query(
        db_order_foods.c.order_id,
        db_order_foods.c.food_id,
        db_order_foods.c.quality,
    ).filter(
        db_order_foods.c.order_id == order_id
    ).all()

    items_dict = {item.food_id: item.quality for item in items}

    if foods is not None:
        result = []
        for food in foods:
            food_data = {
                "id": food.id,
                "foodName": food.food_name,
                "price": food.price,
                "img": food.img,
                "quantity": items_dict.get(food.id, 0)
            }
            result.append(food_data)
        return jsonify(CommonResponse.success(result))
    else:
        return jsonify(CommonResponse.success([]))


@order_view.route("/order/order", methods=["POST"])
def order():
    userId = request.json.get("userId")
    user = UserModel.query.filter_by(id=userId).first()
    # 获取当前用户的购物车
    cart = user.shopping_cart
    # 用户要生成order 的食物id
    food_ids = request.json["food_ids"]
    if food_ids is None:
        return CommonResponse.failure("food_ids is required")
    # 找到中间表的数据
    items = db.session.query(
        db_shopping_cart_foods.c.food_id,
        db_shopping_cart_foods.c.quality
    ).filter(
        db_shopping_cart_foods.c.shopping_cart_id == cart.id
    ).all()

    if items is None:
        return CommonResponse.failure("No food has been selected")
    else:
        temp_foods = []
        sum = 0
        for item in items:
            food = FoodModel.query.filter_by(id=item.food_id).first()
            temp_price = item.quality * food.price
            obj = {
                "foodId": food.id,
                "quantity": item.quality
            }
            temp_foods.append(obj)
            sum += temp_price
        order = OrderModel()
        order.order_time = datetime.utcnow()
        order.user_id = userId
        order.status = 1
        order.total = sum

        try:
            db.session.add(order)
            db.session.commit()

            for item in temp_foods:
                db.session.execute(
                    db_order_foods.insert().values(order_id=order.id, food_id=item["foodId"], quality=item["quantity"]))
                db.session.commit()
            return jsonify(CommonResponse.success("Added"))
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return jsonify(CommonResponse.failure(message=str(e))), 500
        return jsonify(CommonResponse.success("error"))
