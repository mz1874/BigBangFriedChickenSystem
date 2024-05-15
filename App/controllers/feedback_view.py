from flask import Blueprint, jsonify, request
from App.common.decorators import requires_permission
from App.extension import db
from App.common.common_response import CommonResponse
from App.models.user_model import UserModel
from App.models.role_model import RoleModel
from App.models.food_category_model import FoodCategory

feedback_view = Blueprint('feedback', __name__)


@feedback_view.route("/feedback/page", method =["GET"])
def feedback_page():
    pass;


@feedback_view.route("/feedback/add", method =["POST"])
def addFeedback():
    pass;


@feedback_view.route("/feedback/delete", method =["POST"])
def deleteFeedback():
    pass
