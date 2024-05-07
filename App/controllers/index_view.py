from werkzeug.exceptions import NotFound
from flask import Blueprint, jsonify, request, render_template, abort, session

from App.common.decorators import requires_permission
from App.models.user_model import UserModel
from App.extension import login_manager
from App.common.common_response import CommonResponse
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, \
    user_unauthorized

home_view = Blueprint('home', __name__)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


@home_view.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = UserModel.query.filter(UserModel.username == username).first()
    roles = user.roles
    result = [role.role_name for role in roles]
    if not user:
        return jsonify(CommonResponse.failure("Invalid username or password"))
    else:
        if password == user.password:
            session["role" + str(user.id)] = result
            login_user(user)
            return jsonify(CommonResponse.success("Successfully logged in"))
        return jsonify({'message': 'Invalid username or password'}), 401

    """
    User Login function 
    """


@home_view.route('/dashboard')
@login_required
def dashboard():
    return jsonify({'message': 'Welcome to the dashboard', 'username': current_user.id})


@home_view.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})
"""
Logout function 
"""


@home_view.route('/current_user', methods=['GET'])
@requires_permission('admin')
def current_user_info():
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        roles = session.get("role" + str(user_id), [])
        return jsonify({'user_id': user_id, 'roles': roles})
    else:
        return jsonify({'message': 'No user logged in'})
"""
Testing access requires_permission admin
"""