from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc, func
import datetime

from .model import ProductCategories
from blueprints import db, app

from flask_jwt_extended import jwt_required

bp_category = Blueprint('the_category', __name__)  
api = Api(bp_category)


    
class CategoryList(Resource):
    def __init__(self):
        pass

    def get(self):

        product_categories = ProductCategories.query.filter_by(deleted=False).all()


        results = []
       
        for product_category in product_categories:
            results.append(marshal(product_category, ProductCategories.response_fields))

        return results, 200


class CategoryResource(Resource):
    def __init__(self):
        pass

    def get(self,id):
        product_category = ProductCategories.query.filter(ProductCategories.id==id).filter(ProductCategories.deleted==False).all()                   
        if product_category is not None:
            return marshal(product, ProductCategories.response_fields), 200
        else:
            return {'status': 'NOT FOUND'}, 404

api.add_resource(CategoryList,'')
api.add_resource(CategoryResource,'/<id>')


