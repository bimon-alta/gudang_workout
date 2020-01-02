from blueprints import db
from flask_restful import fields
import datetime

class ShippingAdresses(db.Model):
    __tablename__ = "shipping_addresses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_detail_id = db.Column(db.Integer, db.ForeignKey("sale_details.id"), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    province = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.Integer, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    deleted = db.Column(db.Boolean, default=False)

    
    response_fields = {
        'id' : fields.Integer,
        'sale_detail_id' : fields.Integer,
        'address' : fields.String,
        'district' : fields.String,
        'city' : fields.String,
        'province' : fields.String,
        'postal_code' : fields.Integer,
        
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime,
        'deleted' : fields.Boolean

    }

    def __init__(self, sale_detail_id, address, district, city, province, postal_code=0):
        self.sale_detail_id = sale_detail_id
        self.address = address
        self.district = district
        self.city = city
        self.province = province
        self.postal_code = postal_code

        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Shipping Address %r>' % self.id