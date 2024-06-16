from flask import Blueprint, jsonify, request
from sqlalchemy import and_

from App.common.decorators import requires_permission
from App.extension import db
from App.common.common_response import CommonResponse
from App.models.user_model import UserModel
from App.models.role_model import RoleModel
from App.models.shopping_cart_model import ShoppingCart

user_view = Blueprint('user_view', __name__)


@user_view.route('/user/selectUserById', methods=['GET'])
def get_user_by_id():
    user_id = request.args.get('userId')
    try:
        user = UserModel.query.filter_by(id=user_id).first()
        if user:
            user_data = {
                'id': user.id,
                'userName': user.username,
                'tel': user.tel,
                'address': user.address,
                'birthDay': user.brithDay,
                'email': user.email,
            }
            return jsonify(CommonResponse.success(user_data)), 200
        else:
            return jsonify(CommonResponse.failure(message="User not found")), 404
    except Exception as e:
        return jsonify(CommonResponse.failure(message=str(e))), 500


@user_view.route('/user/page', methods=['GET'])
def select_all_user():
    page = request.args.get('page', 1, type=int)  # 默认为第一页
    per_page = request.args.get('per_page', 20, type=int)  # 每页显示数量，默认为10
    username = request.args.get('username')  # 获取查询参数中的用户名

    # 构建查询
    query = UserModel.query.filter(and_(UserModel.username != 'admin', UserModel.s_active == 1))
    if username:
        query = query.filter(UserModel.username == username)

    # 分页处理
    users = query.paginate(page=page, per_page=per_page, error_out=False)

    # 构建返回结果
    response_data = {
        'items': [{'id': user.id, 'userName': user.username, 'tel': user.tel, 'address': user.address, "birthDay":user.brithDay} for user in users.items],
        'total': users.total,
        'page': page,
        'per_page': per_page,
        'pages': users.pages,
        'has_prev': users.has_prev,
        'has_next': users.has_next,
        'prev_num': users.prev_num,
        'next_num': users.next_num
    }

    return jsonify(CommonResponse.success(response_data))

@user_view.route("/updateUser", methods=["POST"])
def update_user():
    request_data = request.get_json()
    if not request_data:
        return jsonify(CommonResponse.failure(message="Request data is empty")), 400

    user_id = request_data.get("user_id")
    tel = request_data.get("tel")
    address = request_data.get("address")
    birthDay = request_data.get("birthDay")
    email = request_data.get("email")
    password = request_data.get("password")

    if not all([user_id, tel,birthDay, email, address]):
        return jsonify(CommonResponse.failure(message="All fields are required")), 400

    try:
        user = UserModel.query.filter_by(id=user_id).first()
        if user:
            user.tel = tel
            user.address = address
            user.brithDay = birthDay
            user.email = email
            if password is not None:
                user.password = password
            else:
                user.password = user.password
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
    user.s_active = 0
    if user is not None:
        db.session.commit()
        return jsonify(CommonResponse.success(message="Delete successful"))
    else:
        raise Exception("Invalid User id")


@user_view.route('/register', methods=['POST'])
def add_user():
    request_data = request.get_json()
    # Check if the request data is empty
    if not request_data:
        return jsonify(CommonResponse.failure(message="Request data is empty")), 400

    username = request_data.get('username')
    password = request_data.get('password')
    role_id = request_data.get('role')
    tel = request_data.get("telephone")
    email = request_data.get('email')
    address = request_data.get('address')
    birthDay = request_data.get('birthDay')
    # Ensure all required fields are provided
    if not all([username, password, email, tel, address, role_id, birthDay]):
        return jsonify(CommonResponse.failure(message="All fields are required")), 400

    # Fetch the role based on role_id
    role = RoleModel.query.filter_by(id=role_id).first()
    if not role or role.role_name == "admin":
        return jsonify(CommonResponse.failure(message="Invalid role_id")), 400

    try:
        # Create new shopping cart and user
        cart = ShoppingCart()
        user = UserModel(username=username, password=password, address=address, shopping_cart=cart, tel=tel,
                         email=email, s_active = 1, brithDay = birthDay)

        # Add the role to the user's roles
        user.user_roles.append(role)

        # Add the user to the session and commit
        db.session.add(user)
        db.session.commit()

        return jsonify(CommonResponse.success(message="User added successfully")), 200

    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        return jsonify(CommonResponse.failure(message=str(e))), 500


@user_view.route("/addRoleToUser", methods=["POST"])
def add_roles_to_user():
    request_data = request.get_json()
    if not request_data:
        return jsonify(CommonResponse.failure(message="Request data is empty")), 400
    role_id = request_data.get("roleId")
    user_id = request_data.get("userId")
    if not user_id:
        return jsonify(CommonResponse.failure(message="userId is empty")), 400
    if not role_id:
        return jsonify(CommonResponse.failure(message="roleId is empty")), 400
    try:
        role = RoleModel.query.filter_by(id=role_id).first()
        if not role:
            return jsonify(CommonResponse.failure(message="Could not find the role")), 400
        current_user = UserModel.query.filter_by(id=user_id).first()

        if not current_user:
            return jsonify(CommonResponse.failure(message="Could not find the user")), 400

        current_user.user_roles.append(role)  # 将角色添加到用户中
        db.session.commit()
        return jsonify(CommonResponse.success(message="Role added to user successfully")), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(CommonResponse.failure(message=str(e))), 500
