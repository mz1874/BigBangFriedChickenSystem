from flask import Blueprint, jsonify, request
from App.common.decorators import requires_permission
from App.extension import db
from App.common.common_response import CommonResponse
from App.models.food_category_model import FoodCategory

food_view = Blueprint('food', __name__)


@food_view.route("/food/page", methods=["GET"])
def page():
    pass


@food_view.route("/food/add", methods=["POST"])
def food_add():
    pass


@food_view.route("/food/delete", methods=["POST"])
def food_delete():
    pass


@food_view.route("/food/update", methods=["POST"])
def food_update():
    pass
