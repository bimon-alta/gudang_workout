from blueprints import db
from flask_restful import fields
import datetime

class Payments(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sales.id"), nullable=False)
    bank_account_id = db.Column(db.Integer, db.ForeignKey("bank_accounts.id"), nullable=False)
    total_to_transfer = db.Column(db.Integer, nullable=False)
    expired_time = db.Column(db.DateTime, nullable=False)
    url_proof_img = db.Column(db.String(255), default='')
    

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    deleted = db.Column(db.Boolean, default=False)

    
    response_fields = {
        'id' : fields.Integer,
        'sale_id' : fields.Integer,
        'bank_account_id' :  fields.Integer,
        'total_to_transfer' :  fields.Integer,
        'expired_time' : fields.DateTime,
        'url_proof_img' : fields.String,

        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime,
        'deleted' : fields.Boolean

    }
    def __init__(self, sale_id, bank_account_id, total_to_transfer, expired_time, url_proof_img):
        self.sale_id = sale_id
        self.bank_account_id = bank_account_id
        self.total_to_transfer = total_to_transfer
        self.expired_time = expired_time
        self.url_proof_img = url_proof_img

        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Payments %r>' % self.id