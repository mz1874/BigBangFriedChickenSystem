from App.extension import db


db_roles_auths = db.Table('db_roles_auths',
                               db.Column('role_id', db.Integer, db.ForeignKey('tb_role.id'), primary_key=True),
                               db.Column('auth_id', db.Integer, db.ForeignKey('tb_authorization.id'), primary_key=True))
class RoleModel(db.Model):
    __tablename__ = 'tb_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'))
    roles_auths = db.relationship('AuthorizationModel',backref='Roles', lazy='dynamic', secondary=db_roles_auths)