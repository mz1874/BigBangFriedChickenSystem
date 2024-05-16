from App.extension import db


class FoodModel(db.Model):
    __tablename__ = 'tb_food'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=True)
    img = db.Column(db.String(100), nullable=False, unique=True)
    info = db.Column(db.String(200), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('tb_category.id'), nullable=False)