from App.extension import db


class UserModel(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.Boolean, nullable=True)
    address = db.Column(db.String(100), nullable=False)

    # 一对多
    roles = db.relationship('RoleModel', backref='user', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)