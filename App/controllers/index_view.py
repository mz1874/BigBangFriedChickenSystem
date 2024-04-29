from werkzeug.exceptions import NotFound
from flask import Blueprint, jsonify, request, render_template, abort
from App.extension import cache

home_view = Blueprint('home', __name__)


@home_view.route("/index", methods=['GET'])
def index():
    return "ok"