from blueprints import db
from flask_restful import fields
import datetime

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    the_password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    is_merchant = db.Column(db.Boolean, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    deleted = db.Column(db.Boolean, default=False)

    response_fields = {
        'id': fields.Integer,
        'user_name': fields.String,
        'email': fields.String,
        'created_at': fields.DateTime
    }

    jwt_claims_fields = {
        'user_name' : fields.String,
        'is_admin': fields.Boolean
    }

    def __init__(self, user_name, email, the_password, is_admin, is_merchant):
        self.user_name = user_name
        self.email = email
        self.the_password = the_password
        self.is_admin = is_admin
        self.is_merchant = is_merchant
        
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Users %r>' % self.id