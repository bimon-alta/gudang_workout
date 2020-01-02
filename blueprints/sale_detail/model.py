from blueprints import db
from flask_restful import fields
import datetime

class SaleDetails(db.Model):
    __tablename__ = "sale_details"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sales.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    qty = db.Column(db.Integer, default=0)
    price_on_sale = db.Column(db.Integer, default=0)
    discount_amount = db.Column(db.Integer, default=0)
    total_shipping_fee = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    is_shipped = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    deleted = db.Column(db.Boolean, default=False)

    
    response_fields = {
        'id' : fields.Integer,
        'sale_id' : fields.Integer,
        'product_id' : fields.Integer,
        'qty' : fields.Integer,
        'price_on_sale' : fields.Integer,
        'discount_amount' : fields.Integer,
        'total_shipping_fee' : fields.Integer,
        'total' : fields.Integer,
        'is_shipped' : fields.Boolean,

        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime,
        'deleted' : fields.Boolean

    }

    def __init__(self, sale_id, product_id, qty, price_on_sale,discount_amount, total_shipping_fee, total, is_shipped=False):
        self.sale_id = sale_id
        self.product_id = product_id
        self.qty = qty
        self.price_on_sale = price_on_sale
        self.discount_amount = discount_amount
        self.total_shipping_fee = total_shipping_fee
        self.total = total
        self.is_shipped = is_shipped

        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Sale Details %r>' % self.id