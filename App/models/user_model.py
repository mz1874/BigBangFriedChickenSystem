from App.extension import db

db_user_roles = db.Table('db_user_roles',
                         db.Column('user_id', db.Integer, db.ForeignKey('tb_user.id'), primary_key=True),
                         db.Column('role_id', db.Integer, db.ForeignKey('tb_role.id'), primary_key=True))

db_user_order = db.Table('db_user_order',
                         db.Column('user_id', db.Integer, db.ForeignKey('tb_user.id'), primary_key=True),
                         db.Column('order_id', db.Integer, db.ForeignKey('tb_order.id'), primary_key=True))


class UserModel(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.Boolean, nullable=True)
    address = db.Column(db.String(100), nullable=False)
    user_roles = db.relationship("RoleModel", backref='users', lazy='dynamic', secondary=db_user_roles)
    # 一对多
    orders  = db.relationship('OrderModel', backref='user', lazy=True)
    shopping_cart = db.relationship('ShoppingCart', backref='user', uselist=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
