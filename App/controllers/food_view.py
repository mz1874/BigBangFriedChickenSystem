from flask import Blueprint, jsonify, request
import os
from App.common.common_response import CommonResponse
from App.models.food_model import FoodModel
from werkzeug.utils import secure_filename
from App.common.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from App.extension import db
from App.models.food_category_model import FoodCategory

food_view = Blueprint('food', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@food_view.route("/food/page", methods=["GET"])
def page():
    pass


@food_view.route("/food/add", methods=["POST"])
def food_add():
    request_data = request.get_json()
    if request_data is not None:
        food_name = request_data.get("foodName")
        src = request_data.get("src")
        food_category_id = request_data.get("foodCategoryId")
        price = request_data.get("price")
        info = request_data.get("info")
        if not all([food_name, src, food_category_id, price,info]):
            return CommonResponse.failure("All fields are required")
        else:
            category = FoodCategory.query.filter_by(id=food_category_id).first()
            if category is not None:
                food = FoodModel()
                food.food_name = food_name
                food.food_category = category
                food.price = price
                food.img = src
                food.info = info
                try:
                    db.session.add(food)
                    db.session.commit()
                    return CommonResponse.success("Add food successfully")
                except Exception as e:
                    db.session.rollback()
                    db.session.rollback()
                    return CommonResponse.failure("Add food error", 400)
            else:
                return CommonResponse.failure("Food category error", 400)


@food_view.route('/food/upload', methods=['POST'])
def food_image_upload():
    if 'foodImage' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['foodImage']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200
    else:
        return jsonify({"message": "Invalid file type"}), 400


@food_view.route("/food/delete", methods=["POST"])
def food_delete():
    request_data = request.get_json()
    if request_data is not None:
        id = request_data.get("foodId")
        if id is None:
            CommonResponse.failure("foodId is empty", 400)
        else:
            try:
                food = FoodModel.query.filter_by(id=id).first()
                if food is not None:
                    db.session.delete(food)
                    db.session.commit()
                    return CommonResponse.success("Food has been deleted", 200)
                else:
                    return CommonResponse.failure("Food id is invalid", 400)
            except Exception as e:
                db.session.rollback()
                db.session.flush()
                return jsonify(CommonResponse.failure(message=str(e))), 500
    else:
        return CommonResponse.failure("Request body is empty", 400)


@food_view.route("/food/query", methods=["GET"])
def food_query():
    food_id = request.args.get("foodId")
    if food_id is None:
        return CommonResponse.failure("Food ID is required", 400)

    food = FoodModel.query.get(food_id)
    if food is not None:
        data = {
            "foodId": food.id,
            "foodName": food.food_name,
            "src": food.img,
            "foodCategoryId": food.food_category.id,
            "price": food.price,
            "info": food.info
        }
        return CommonResponse.success(data)
    else:
        return CommonResponse.failure("Food not found", 404)


@food_view.route("/food/update", methods=["POST"])
def food_update():
    request_data = request.get_json()
    if request_data is not None:
        food_id = request_data.get("foodId")
        food_name = request_data.get("foodName")
        price = request_data.get("price")
        info = request_data.get("info")
        src = request_data.get("src")
        category = request_data.get("category")
        if not all([food_id, food_name, price, info, category]):
            return jsonify(CommonResponse("All files are required", 400))
        existed_food = FoodModel.query.get(food_id)
        new_category = FoodCategory.query.filter_by(id=category).first()
        if existed_food and new_category:
            existed_food.food_name = food_name
            existed_food.price = price
            existed_food.info = info
            existed_food.category_id = new_category.id
            existed_food.img = src
            try:
                db.session.commit()
                return jsonify(CommonResponse.success("Updated food successfully"))
            except Exception as e:
                db.session.rollback()
                return jsonify(CommonResponse.failure(message=str(e))), 500
        else:
            return jsonify(CommonResponse.failure("Food not found", 404))
    else:
        return jsonify(CommonResponse.failure("Request body is empty", 400))