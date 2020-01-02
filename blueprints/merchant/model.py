from blueprints import db
from flask_restful import fields
import datetime

class MerchantProfiles(db.Model):
    __tablename__ = "merchant_profiles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  
    store_name = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    province = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.Integer, nullable=True)
    bank_name = db.Column(db.String(255), nullable=False)
    bank_account_name = db.Column(db.String(255), nullable=False)
    bank_account_no = db.Column(db.String(255), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    deleted = db.Column(db.Boolean, default=False)

    
    response_fields = {
        'user_id' : fields.Integer,
        'store_name' : fields.String,
        'address' : fields.String,
        'district' : fields.String,
        'city' : fields.String,
        'province' : fields.String,
        'postal_code' : fields.Integer,
        'bank_name' : fields.String,
        'bank_account_name' : fields.String,
        'bank_account_no' : fields.String,
        
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime,
        'deleted' : fields.Boolean
    }

    def __init__(self, user_id, store_name, address, district, city, province, postal_code, bank_name, bank_account_name, bank_account_no ):
        self.user_id = user_id
        self.store_name = store_name
        self.address = address
        self.district = district
        self.city = city
        self.province = province
        self.postal_code = postal_code
        self.bank_name = bank_name
        self.bank_account_name = bank_account_name
        self.bank_account_no = bank_account_no

        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<MerchantProfile %r>' % self.user_id