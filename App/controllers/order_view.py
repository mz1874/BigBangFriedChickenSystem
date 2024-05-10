from werkzeug.exceptions import NotFound
from flask import Blueprint, jsonify, request, render_template, abort, session

from App.common.decorators import requires_permission
from App.models.user_model import UserModel
from App.extension import login_manager
from App.common.common_response import CommonResponse
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, \
    user_unauthorized

order_view = Blueprint('order_view', __name__)


@order_view.route("/order/selectOrderByUserId", methods=["GET"])
def selectOrder():
    user_id = current_user.id
    user = UserModel.query.filter_by(id = user_id).first()
    if user is not None:
        orders = user.user_orders
