from flask import Blueprint, jsonify, request
from App.common.decorators import requires_permission
from App.extension import db
from App.common.common_response import CommonResponse
from App.models.user_model import UserModel
from App.models.role_model import RoleModel
from App.models.food_category_model import FoodCategory

food_category_view = Blueprint('food_category', __name__)


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
            return
        except Exception as e:
            db.session.rollback()
            db.session.flush()
    else:
        return jsonify(CommonResponse.failure("Could not find this food category")), 400
