from flask import Blueprint, jsonify, request
from App.common.common_response import CommonResponse
from App.extension import db
from App.models.feedback_model import FeedbackModel

feedback_view = Blueprint('feedback', __name__)


@feedback_view.route("/feedback/page", methods=["GET"])
def feedback_page():
    pass;


@feedback_view.route("/feedback/add", methods=["POST"])
def addFeedback():
    request_data = request.get_json()
    if not request_data:
        return jsonify(CommonResponse.failure("Request body is empty")), 400
    name = request_data.get("name")
    email = request_data.get("email")
    category = request_data.get("category")
    visit_type = request_data.get("visitType")
    time_visit = request_data.get("timeVisit")
    date_visit = request_data.get("dataVisit")
    subject = request_data.get("subject")
    message = request_data.get("message")
    if not all([name, email, category, visit_type, time_visit, date_visit, subject, message]):
        return CommonResponse.failure("All fields are required")
    feed_back = FeedbackModel(name=name, email=email, category=category, visit_type=visit_type, time_visit=time_visit,
                              date_visit=date_visit, subject=subject, message=message)
    try:
        db.session.add(feed_back)
        db.session.commit()
        return jsonify(CommonResponse.success("Add feedback successful"))
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify(CommonResponse.failure(message=str(e))), 500


@feedback_view.route("/feedback/delete", methods=["POST"])
def deleteFeedback():
    pass
