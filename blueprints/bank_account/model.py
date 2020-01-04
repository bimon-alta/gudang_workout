from blueprints import db
from flask_restful import fields
import datetime

class BankAccounts(db.Model):
    __tablename__ = "bank_accounts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bank_name = db.Column(db.String(255), nullable=False)
    account_name = db.Column(db.String(255), nullable=False)
    account_no = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    deleted = db.Column(db.Boolean, default=False)

    
    response_fields = {
        'id' : fields.Integer,
        'bank_name' : fields.String,
        'account_name' : fields.String,
        'account_no' : fields.String,

        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime,
        'deleted' : fields.Boolean

    }

    payment_info_fields = {
        'id' : fields.Integer,
        'bank_name' : fields.String,
        'account_name' : fields.String,
        'account_no' : fields.String
    }

    def __init__(self, bank_name, account_name, account_no):
        self.bank_name = bank_name
        self.account_name = account_name
        self.account_no = account_no

        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Sale Details %r>' % self.id