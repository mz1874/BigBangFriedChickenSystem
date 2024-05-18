from App.extension import db
from enum import Enum
from sqlalchemy import Enum as EnumType

class FeedbackModel(db.Model):
    __tablename__ = 'tb_feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    tel = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    visit_type = db.Column(db.String(60), nullable=False)
    time_visit = db.Column(db.String(60), nullable=False)
    date_visit = db.Column(db.String(20),nullable=False)
    subject = db.Column(db.String(60), nullable=False)
    message = db.Column(db.String(255), nullable=False)