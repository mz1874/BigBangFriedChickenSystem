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
        if not all([food_name, src, food_category_id, price]):
            return CommonResponse.failure("All fields are required")
        else:
            category = FoodCategory.query.filter_by(id=food_category_id).first()
            if category is not None:
                food = FoodModel()
                food.food_name = food_name
                food.food_category = category
                food.price = price
                food.img = src
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
    pass


@food_view.route("/food/update", methods=["POST"])
def food_update():
    pass
