from blueprints import db
from flask_restful import fields
import datetime

class ProductCategories(db.Model):
    __tablename__ = "product_categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    deleted = db.Column(db.Boolean, default=False)

    
    response_fields = {
        'id' : fields.Integer,
        'name' : fields.String,
        
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime,
        'deleted' : fields.Boolean,
    }

    def __init__(self, name):
        self.name = name
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Product Category %r>' % self.id