from flask import Blueprint, jsonify, request
from App.common.decorators import requires_permission
from App.extension import db
from App.common.common_response import CommonResponse
from App.models.user_model import UserModel

user_view = Blueprint('user_view', __name__)


@user_view.route('/selectAllUser', methods=['GET'])
@requires_permission("admin")
def select_all_user():
    users = UserModel.query.filter(UserModel.username != 'admin')
    result = [{'id': user.id, 'userName': user.username, 'sex': user.sex, 'address': user.address} for user in users]
    return jsonify(CommonResponse.success(result))


@user_view.route("/updateUser", methods=["PUT"])
def update_user():
    request_data = request.get_json()
    if not request_data:
        return jsonify(CommonResponse.failure(message="Request data is empty")), 400

    user_id = request_data.get("user_id")
    username = request_data.get("username")
    sex = request_data.get("sex")
    address = request_data.get("address")

    if not all([user_id, username, sex, address]):
        return jsonify(CommonResponse.failure(message="All fields are required")), 400

    try:
        user = UserModel.query.filter_by(id=user_id).first()
        if user:
            user.username = username
            user.sex = sex
            user.address = address
            db.session.commit()
            return jsonify(CommonResponse.success(message="User updated successfully")), 200
        else:
            return jsonify(CommonResponse.failure(message="User not found")), 404
    except Exception as e:
        db.session.rollback()
        return jsonify(CommonResponse.failure(message=str(e))), 500


@user_view.route('/deleteUser', methods=["POST"])
def delete_user_by_id():
    request_data = request.get_json()
    user_id = request_data.get("user_id")
    user = UserModel.query.filter_by(id=user_id).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return jsonify(CommonResponse.success(message="Delete successful"))
    else:
        raise Exception("Invalid User id")


@user_view.route('/register', methods=['POST'])
def add_user():
    request_data = request.get_json()
    # 检查请求数据是否为空
    if not request_data:
        return jsonify(CommonResponse.failure(message="Request data is empty")), 400
    username = request_data.get('username')
    password = request_data.get('password')
    sex = request_data.get('sex')
    address = request_data.get('address')
    if not all([username, password, sex, address]):
        return jsonify(CommonResponse.failure(message="All fields are required")), 400
    try:
        user = UserModel(username=username, password=password, sex=sex, address=address)
        db.session.add(user)
        db.session.commit()
        return jsonify(CommonResponse.success(message="User added successfully")), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(CommonResponse.failure(message=str(e))), 500
