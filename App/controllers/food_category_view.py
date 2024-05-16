from flask import Blueprint, jsonify, request
from App.common.decorators import requires_permission
from App.extension import db
from App.common.common_response import CommonResponse
from App.models.user_model import UserModel
from App.models.role_model import RoleModel
from App.models.food_category_model import FoodCategory

food_category_view = Blueprint('food_category', __name__)

@food_category_view.route("/foodCategory/list", methods=["GET"])
def list_all_food_category():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('count', 10, type=int)
    # 分页查询
    pagination = FoodCategory.query.paginate(page=page, per_page=per_page)

    # 构造返回结果
    categories = pagination.items
    result = [{"id": category.id, "categoryName": category.category_name} for category in categories]

    return jsonify(CommonResponse.success({
        "items": result,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "has_prev": pagination.has_prev,
        "has_next": pagination.has_next,
        "prev_num": pagination.prev_num,
        "next_num": pagination.next_num
    })), 200

@food_category_view.route("/foodCategory/getFoodsByCategoryId", methods=["GET"])
def list_all_foods_in_category():
    category_id = request.args.get("categoryId")
    if not category_id:
        return jsonify(CommonResponse.failure("categoryId is empty")), 400

    food_category = FoodCategory.query.filter_by(id=category_id).first()
    if not food_category:
        return jsonify(CommonResponse.failure("Category not found")), 404

    foods = food_category.foods
    # 这里假设 foods 是一个列表，包含食物对象，您需要将其转换为可序列化的格式，比如字典列表
    foods_list = [{"id": food.id, "name": food.food_name, "img": food.img, "info": food.info, "price":food.price} for food in foods]

    return jsonify(CommonResponse.success("Foods retrieved successfully", data=foods_list))



@food_category_view.route("/foodCategory/add", methods=["POST"])
def add_food_category():
    request_data = request.get_json()
    if not request_data:
        return jsonify(CommonResponse.failure("Request body is empty")), 400
    category_name = request_data.get("category")
    if not category_name:
        return jsonify(CommonResponse.failure("Category is empty")), 400

    if FoodCategory.query.filter_by(category_name=category_name).first():
        return jsonify(CommonResponse.failure("Category already exists")), 400

    try:
        new_category = FoodCategory(category_name=category_name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify(CommonResponse.success("Category added successfully")), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(CommonResponse.failure(str(e))), 500


@food_category_view.route("/foodCategory/delete", methods=["POST"])
def delete_food_category():
    request_data = request.get_json()
    if not request_data:
        return jsonify(CommonResponse.failure("Request body is empty")), 400
    category_id = request_data.get("categoryId")
    if not category_id:
        return jsonify(CommonResponse.failure("categoryId is empty")), 400
    food_category = FoodCategory.query.filter_by(id=category_id).first()
    if food_category is not None :
        try:
            db.session.delete(food_category)
            db.session.commit()
            return CommonResponse.success("Category has been deleted successfully"), 200
        except Exception as e:
            db.session.rollback()
            db.session.flush()
    else:
        return jsonify(CommonResponse.failure("Could not find this food category")), 400



@food_category_view.route("/foodCategory/update", methods=["POST"])
def update_food_category():
    request_data = request.get_json()
    if not request_data:
        return jsonify(CommonResponse.failure("Request body is empty")), 400
    category_id = request_data.get("categoryId")
    category_name = request_data.get("categoryName")
    if category_id is None or category_name is None:
        return jsonify(CommonResponse.failure("categoryId or categoryName is empty")), 400
    food_category = FoodCategory.query.filter_by(id=category_id).first()
    uf
    if food_category is not None :
        try:
            food_category.category_name = category_name
            db.session.commit()
            return jsonify(CommonResponse.success("category update successful!"))
        except Exception as e:
            db.session.rollback()
            db.session.flush()
    else:
        return jsonify(CommonResponse.failure("Could not find this food category")), 400

