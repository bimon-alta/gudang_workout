from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
import datetime

from blueprints import db, app
from blueprints.product.model import Products
from blueprints.product_category.model import ProductCategories

from flask_jwt_extended import jwt_required

bp_home = Blueprint('the_home', __name__)  
api = Api(bp_home)


class BookResource(Resource):
    def __init__(self):
        pass
    
    def get(self):
        result = []

        #membuat daftar product terbaru
        new_products = Products.query.filter(Products.deleted==False).order_by(desc(Products.created_at)).all()
        list_new_product = []
        for new_product in new_products.limit(20).offset(0).all():
            list_new_product.append(marshal(new_product, Products.response_fields))

        result.append({'new_products':list_new_product})

        #membuat daftar product terlaris
        most_sellable_products = Products.query.filter(Products.deleted==False).order_by(desc(Products.created_at)).all()
        list_most_sellable_product = []
        for new_product in new_products.limit(20).offset(0).all():
            list_most_sellable_product.append(marshal(most_sellable_products, Products.response_fields))

        result.append({'most_sellable_products':list_most_sellable_product})

        return result, 200



    

api.add_resource(BookResource,'')   

