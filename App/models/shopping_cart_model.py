from App.extension import db

db_shopping_cart_foods = db.Table('db_shopping_cart_foods',
                                  db.Column('shopping_cart_id', db.Integer, db.ForeignKey('tb_shopping_cart.id'),
                                            primary_key=True),
                                  db.Column('food_id', db.Integer, db.ForeignKey('tb_food.id'), primary_key=True))


class ShoppingCart(db.Model):
    __tablename__ = 'tb_shopping_cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shopping_cart_foods = db.relationship("FoodModel", backref='shopping_cart', lazy='dynamic',
                                          secondary=db_shopping_cart_foods)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), unique=True, nullable=False)
