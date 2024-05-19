from flask import Blueprint, jsonify, request
from App.common.common_response import CommonResponse
from App.extension import db
from App.models.feedback_model import FeedbackModel

feedback_view = Blueprint('feedback', __name__)


@feedback_view.route("/feedback/page", methods=["GET"])
def feedback_page():
    page = request.args.get("page", 1, type=int)
    count = request.args.get("count", 20, type=int)
    feedbacks_paginated = FeedbackModel.query.paginate(page=page, per_page=count, max_per_page=100, error_out=False)

    if feedbacks_paginated.items:
        result = [{"id": feedback.id, "name": feedback.name, "email": feedback.email, "category": feedback.category,
                   "visitType": feedback.visit_type, "timeVisit": feedback.time_visit, "dateVisit": feedback.date_visit,
                   "subject": feedback.subject, "message": feedback.message, "tel": feedback.tel} for feedback in feedbacks_paginated.items]

        return jsonify(CommonResponse.success({
            "items": result,
            "total": feedbacks_paginated.total,
            "page": feedbacks_paginated.page,
            "pages": feedbacks_paginated.pages,
            "has_prev": feedbacks_paginated.has_prev,
            "has_next": feedbacks_paginated.has_next,
            "prev_num": feedbacks_paginated.prev_num,
            "next_num": feedbacks_paginated.next_num
        })), 200
    else:
        return jsonify(CommonResponse.success({
            "feedbacks": [],
            "pagination": {
                "page": page,
                "per_page": count,
                "total_pages": 0,
                "total_items": 0
            }
        }))


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
    tel = request_data.get("tel")
    if not all([name, email, category, visit_type, time_visit, date_visit, subject, message, tel]):
        return CommonResponse.failure("All fields are required")
    feed_back = FeedbackModel(name=name, email=email, category=category, visit_type=visit_type, time_visit=time_visit,
                              date_visit=date_visit, subject=subject, message=message,tel = tel)
    try:
        db.session.add(feed_back)
        db.session.commit()
        return jsonify(CommonResponse.success("Add feedback successful"))
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify(CommonResponse.failure(message=str(e))), 500


@feedback_view.route("/feedback/<int:feedback_id>", methods=["GET"])
def get_feedback_by_id(feedback_id):
    feedback = FeedbackModel.query.filter_by(id=feedback_id).first()
    if feedback:
        result = {
            "id": feedback.id,
            "name": feedback.name,
            "email": feedback.email,
            "category": feedback.category,
            "visitType": feedback.visit_type,
            "timeVisit": feedback.time_visit,
            "dateVisit": feedback.date_visit,
            "subject": feedback.subject,
            "message": feedback.message,
            "tel": feedback.tel
        }
        return jsonify(CommonResponse.success(result)), 200
    else:
        return jsonify(CommonResponse.failure("Feedback not found")), 404


@feedback_view.route("/feedback/delete", methods=["POST"])
def deleteFeedback():
    pass
