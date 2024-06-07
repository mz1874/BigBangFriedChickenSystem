from App.extension import db
from datetime import datetime

db_shopping_cart_foods = db.Table(
    'db_shopping_cart_foods',
    db.Column('shopping_cart_id', db.Integer, db.ForeignKey('tb_shopping_cart.id'), primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('tb_food.id'), primary_key=True),
    db.Column('quality', db.Integer),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)  # 新增时间字段
)


class ShoppingCart(db.Model):
    __tablename__ = 'tb_shopping_cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), nullable=True)
    foods = db.relationship("FoodModel", secondary=db_shopping_cart_foods, lazy='dynamic',
                            backref="shopping_cart")
