from App.extension import db


class FoodCategory(db.Model):
    __tablename__ = 'tb_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), nullable=False, unique=True)
    foods = db.relationship('FoodModel', backref='food_category', lazy=True)