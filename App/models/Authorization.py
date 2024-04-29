from App.extension import db

class AuthorizationModel(db.Model):
    __tablename__ = 'tb_authorization'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auth_name = db.Column(db.String(50),nullable=False)
    resource_path = db.Column(db.String(100),nullable=False)
