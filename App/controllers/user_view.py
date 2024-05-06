from flask import Blueprint, jsonify, request

from App.common.decorators import requires_permission
from App.extension import db

from App.common.CommonResponse import CommonResponse
from App.models.UserModel import UserModel

user_view = Blueprint('user_view', __name__)


@user_view.route('/selectAllUser', methods=['GET'])
def select_all_user():
    users = UserModel.query.filter(UserModel.username != 'admin')
    result = [{'id': user.id, 'userName': user.username, 'sex': user.sex, 'address': user.address} for user in users]
    return jsonify(result)




"""
查找当前系统的所有用户
"""

@user_view.route('/addUser', methods=['POST'])
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
