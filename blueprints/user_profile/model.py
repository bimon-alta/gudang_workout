from blueprints import db
from flask_restful import fields
import datetime

class UserProfiles(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  
    full_name = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.String(50), nullable=False)
    birth_place = db.Column(db.String(255), nullable=True)
    birth_date = db.Column(db.DateTime, nullable=False)
    phone_no = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    province = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.String(255), nullable=True)
    url_img = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    deleted = db.Column(db.Boolean, default=False)

    


    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'full_name': fields.String,
        'sex': fields.String,
        'birth_place' : fields.String,
        'birth_date' : fields.DateTime, 
        'phone_no': fields.String,
        'address' : fields.String,
        'city' : fields.String,
        'province' : fields.String,
        'bio' : fields.String,
        'url_img' : fields.String,

        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'deleted': fields.Boolean
    }

    def __init__(self, user_id, full_name, sex, birth_place, birth_date, phone_no, address, city, province, bio, url_image):
        self.user_id = user_id
        self.full_name = full_name
        self.sex = sex
        self.birth_place = birth_place
        self.birth_date = birth_date
        self.phone_no = phone_no
        self.address = address
        self.city = city
        self.province = province
        self.bio = bio
        self.url_img = url_image
        
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<UserProfile %r>' % self.user_id