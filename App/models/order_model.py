from datetime import datetime

from App.extension import db

db_order_foods = db.Table('db_order_foods',
                               db.Column('order_id', db.Integer, db.ForeignKey('tb_order.id'), primary_key=True),
                               db.Column('food_id', db.Integer, db.ForeignKey('tb_food.id'), primary_key=True))
class OrderModel(db.Model):
    __tablename__ = 'tb_order'
    id = db.Column(db.Integer, primary_key=True)
    order_time = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), nullable=False)
    order_foods = db.relationship("FoodModel", backref='order', lazy='dynamic', secondary=db_order_foods)
