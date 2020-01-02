from blueprints import db
from flask_restful import fields
import datetime

class Sales(db.Model):
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_bill = db.Column(db.Integer, default=0)
    is_paid = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    deleted = db.Column(db.Boolean, default=False)

    
    response_fields = {
        'id' : fields.Integer,
        'user_id' : fields.Integer,
        'total_bill' : fields.Integer,
        'is_paid' : fields.Boolean,

        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime,
        'deleted' : fields.Boolean

    }

    def __init__(self, user_id, total_bill, is_paid):
        self.user_id = user_id
        self.total_bill = total_bill
        self.is_paid = is_paid
        
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Sales %r>' % self.id