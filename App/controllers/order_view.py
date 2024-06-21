from select import select

from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import load_only, joinedload

from App.common.common_response import CommonResponse
from App.models.food_model import FoodModel
from App.models.user_model import UserModel
from App.models.order_model import OrderModel
from App.extension import db
from App.models.shopping_cart_model import db_shopping_cart_foods
from App.models.order_model import db_order_foods

order_view = Blueprint('order_view', __name__)

@order_view.route("/order/byDriverId", methods=["GET"])
def get_orders_by_driver_id():
    driver_id = request.args.get("driverId", type=int)
    status = request.args.get("status", type=int)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    if not driver_id:
        return jsonify(CommonResponse.failure("driverId is required")), 400

    try:
        # 查询订单并关联用户信息
        query = db.session.query(OrderModel, UserModel.username.label('user_name')) \
            .join(UserModel, UserModel.id == OrderModel.user_id) \
            .filter(OrderModel.driver_id == driver_id)

        # 如果 status 参数存在，添加过滤条件
        if status is not None:
            query = query.filter(OrderModel.status == status)

        # 分页查询
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        orders = pagination.items

        if not orders:
            return jsonify(CommonResponse.success([])), 200

        result = [
            {
                "id": order.OrderModel.id,
                "orderTime": order.OrderModel.order_time.strftime('%Y-%m-%d %H:%M:%S'),
                "total": order.OrderModel.total,
                "status": order.OrderModel.status,
                "username": order.user_name
            } for order in orders
        ]

        # 构建包含分页信息的响应
        pagination_info = {
            "items": result,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "has_prev": pagination.has_prev,
            "has_next": pagination.has_next,
            "prev_num": pagination.prev_num if pagination.has_prev else None,
            "next_num": pagination.next_num if pagination.has_next else None,
        }

        return jsonify(CommonResponse.success(pagination_info)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(CommonResponse.failure(str(e))), 500


@order_view.route("/order/assignDriver", methods=["POST"])
def assign_driver():
    order_id = request.json.get("orderId")
    driver_id = request.json.get("driverId")

    if not order_id:
        return jsonify(CommonResponse.failure("orderId is required")), 400

    if not driver_id:
        return jsonify(CommonResponse.failure("driverId is required")), 400

    try:
        order = OrderModel.query.filter_by(id=order_id).first()
        if not order:
            return jsonify(CommonResponse.failure("Order not found")), 404
        order.driver_id = driver_id
        order.status = 3
        db.session.commit()
        return jsonify(CommonResponse.success("Driver assigned and order status updated successfully"))
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(CommonResponse.failure(str(e))), 500

@order_view.route("/order/page", methods=["GET"])
def page():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('count', 20, type=int)
    orderId = request.args.get('orderId', type=int)
    startTime = request.args.get('startTime', type=str)
    endTime = request.args.get('endTime', type=str)
    status = request.args.get('status', type=int)

    query = OrderModel.query.options(joinedload(OrderModel.user).load_only(UserModel.username)).options(load_only(
        OrderModel.id, OrderModel.order_time, OrderModel.total, OrderModel.status))

    # 处理日期转换
    if startTime and endTime:
        try:
            start_date = datetime.strptime(startTime, "%Y-%m-%d").date()
            end_date = datetime.strptime(endTime, "%Y-%m-%d").date() + timedelta(days=1)
        except ValueError:
            return jsonify(CommonResponse.failure("Invalid date format. Please use 'YYYY-MM-DD'.")), 400
        query = query.filter(OrderModel.order_time.between(start_date, end_date))

    if orderId:
        query = query.filter(OrderModel.id == orderId)

    if status is not None:
        query = query.filter(OrderModel.status == status)

    try:
        # 分页查询
        order_pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        orders = order_pagination.items
        result = [
            {
                "id": order.id,
                "orderTime": order.order_time.strftime('%Y-%m-%d %H:%M:%S'),
                "total": order.total,
                "status": order.status,
                "username": order.user.username,
                "isPickUp": order.isPickUp
            } for order in orders
        ]

        # 构建包含分页信息的响应
        pagination_info = {
            "items": result,
            "total": order_pagination.total,
            "page": order_pagination.page,
            "pages": order_pagination.pages,
            "has_prev": order_pagination.has_prev,
            "has_next": order_pagination.has_next,
            "prev_num": order_pagination.prev_num if order_pagination.has_prev else None,
            "next_num": order_pagination.next_num if order_pagination.has_next else None,
        }

        return jsonify(CommonResponse.success(pagination_info))
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(CommonResponse.failure(str(e))), 500



@order_view.route("/order/selectOrderByUserId", methods=["GET"])
def selectOrder():
    userId = request.args.get("userId")
    user = UserModel.query.filter_by(id=userId).first()
    if user is not None:
        orders = user.orders
        if orders is not None:
            result = [{"id": order.id, "orderTime": order.order_time, "total": order.total, "status": order.status, "isPickUp":order.isPickUp} for
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
    is_pick_up = request.json["pick_up"]
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
        order.isPickUp =is_pick_up

        try:
            db.session.add(order)
            db.session.commit()

            for item in temp_foods:
                db.session.execute(
                    db_order_foods.insert().values(order_id=order.id, food_id=item["foodId"], quality=item["quantity"]))
                db.session.commit()

                db.session.query(db_shopping_cart_foods).filter(
                    db_shopping_cart_foods.c.shopping_cart_id == cart.id).delete()
                db.session.commit()
            return jsonify(CommonResponse.success("Added"))
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return jsonify(CommonResponse.failure(message=str(e))), 500
        return jsonify(CommonResponse.success("error"))


@order_view.route("/order/updateStatus", methods=["POST"])
def update_status():
    order_id = request.json.get("orderId")
    status = request.json.get("status")

    if not order_id:
        return jsonify(CommonResponse.failure("orderId is required")), 400

    if status is None:
        return jsonify(CommonResponse.failure("status is required")), 400

    try:
        order = OrderModel.query.filter_by(id=order_id).first()
        if True is order.isPickUp:
            order.status = 4
        else:
            order.status = status
        if not order:
            return jsonify(CommonResponse.failure("Order not found")), 404
        db.session.commit()
        return jsonify(CommonResponse.success("Order status updated successfully"))
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(CommonResponse.failure(str(e))), 500