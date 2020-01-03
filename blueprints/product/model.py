from blueprints import db
from flask_restful import fields
import datetime

class Products(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("product_categories.id"), nullable=False)   
    default_price = db.Column(db.Integer, nullable=False, default=0)
    brand_name = db.Column(db.String(255), nullable=False)
    country_of_origin = db.Column(db.String(255), nullable=False)
    url_img1 = db.Column(db.String(255), nullable=False)
    url_img2 = db.Column(db.String(255), nullable=False)
    url_img3 = db.Column(db.String(255), nullable=False)
    condition = db.Column(db.String(30), nullable=False, default='baru')
    # weight_kg = db.Column(db.Float(precision='5,2'), nullable=False, default=0)
    weight_gram = db.Column(db.Integer, nullable=False, default=0)
    short_description = db.Column(db.String(255), nullable=False)
    detail_product = db.Column(db.Text, default='')
    is_available = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    deleted = db.Column(db.Boolean, default=False)

    response_fields = {
        'id' : fields.Integer,
        'name' : fields.String,
        'merchant_id' : fields.Integer,
        'category_id' : fields.Integer,
        'default_price' : fields.Integer,
        'brand_name' : fields.String,
        'country_of_origin' : fields.String,
        'url_img1' : fields.String,
        'url_img2' : fields.String,
        'url_img3' : fields.String,
        'condition' : fields.String,
        'weight_gram' : fields.Integer,
        'short_description' : fields.String,
        'detail_product' : fields.String,
        'is_available' : fields.Boolean,

        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime,
        'deleted' : fields.Boolean
    }

    #marshal utk view order list oleh merchant
    order_list_field = {
        'name' : fields.String,
        'category_id' : fields.Integer,
        'url_img1' : fields.String
    }

    #MARSHAL INI HARUSNYA UTK HASIL JOIN, HANYA SAJA MASIH GAGAL
    # join_sale_fields = {
    #     'id' : fields.Integer,
    #     'name' : fields.String,
    #     'total_sold_qty': fields.Float
    # }

    def __init__(self, name, merchant_id, category_id, default_price, brand_name, country_of_origin, url_img1, url_img2, url_img3, condition, weight_gram, short_description, detail_product, is_available=True):
        self.name = name
        self.merchant_id = merchant_id
        self.category_id =  category_id 
        self.default_price = default_price
        self.brand_name = brand_name
        self.country_of_origin = country_of_origin
        self.url_img1 = url_img1
        self.url_img2 = url_img2
        self.url_img3 = url_img3
        self.condition = condition
        self.weight_gram = weight_gram
        self.short_description = short_description
        self.detail_product = detail_product
        self.is_available = is_available

       
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Product %r>' % self.id