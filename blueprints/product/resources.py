from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc, func
import datetime

from .model import Products
from blueprints import db, app
from blueprints.product_category.model import ProductCategories
from blueprints.sale_detail.model import SaleDetails

from flask_jwt_extended import jwt_required

bp_product = Blueprint('the_product', __name__)  
api = Api(bp_product)

# class ProductList(Resource):
#     def __init__(self):
#         pass
    
class ProductList(Resource):
    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('search_keyword', location='args')
        parser.add_argument('category_id', location='args')
        parser.add_argument('orderby', location='args', help='invalid orderby value')
        parser.add_argument('sort', location='args', help='invalid sort value')
        args = parser.parse_args()

        indeks_mulai = (int(args['p']) * int(args['rp'])) - int(args['rp'])



        product_sales = db.session.query(Products, func.sum(SaleDetails.qty).label('total_sold_qty')).filter(Products.deleted==False).join(SaleDetails).group_by(Products.id)
        # for product_sale in product_sales:
        #     print(product_sale.Products.name)


        if args['category_id'] != None:
            product_sales = product_sales.filter(Products.category_id==int(args['category_id']))

        #query untuk pencarian ada di sini
        if args['search_keyword'] != None:
            # db.users.filter(or_(db.users.name=='Ryan', db.users.country=='England'))
            product_sales = product_sales.filter(or_(ProductCategories.name.like("%"+args['search_keyword']+"%"), ProductCategories.short_description.like("%"+args['search_keyword']+"%")))
 

        #sementara diurutkan hanya berdasarkan produk dibuat (terbaru/lama)
        if args['orderby'] is not None:
            #diurutkan produk terbaru (diinput)
            if args['orderby'] == 'created_at':
                product_sales = product_sales.order_by(desc(Products.created_at))
                
            #diurutkan produk terlaris
            elif args['orderby'] == 'total_sold_qty':
                product_sales = product_sales.order_by(desc(product_sales.total_sold_qty))

            #diurutkan produk termahal
            elif args['orderby'] == 'default_price':
                if args['sort'] == 'desc':
                    product_sales = product_sales.order_by(desc(Products.default_price))
                else:
                    #diurutkan produk termurah
                    product_sales = product_sales.order_by(Products.default_price)


        results = []
        # for product_sale in product_sales.limit(int(args['rp'])).offset(indeks_mulai).all():
            # results.append(marshal(product_sale, Products.join_sale_fields))
        # for product_sale in product_sales.all():
        #     results.append(marshal(product_sale, Products.join_sale_fields))

        # print(product_sales[1].name)
        for product_sale in product_sales.limit(int(args['rp'])).offset(indeks_mulai).all():
            product_data = {
                'id' : product_sale.Products.id,
                'name' : product_sale.Products.name,
                'merchant_id' : product_sale.Products.merchant_id,
                'category_id' : product_sale.Products.category_id,
                'default_price' : product_sale.Products.default_price,
                'brand_name' : product_sale.Products.brand_name,
                'country_of_origin' : product_sale.Products.country_of_origin,
                'url_img1' : product_sale.Products.url_img1,
                'url_img2' : product_sale.Products.url_img2,
                'url_img3' : product_sale.Products.url_img3,
                'condition' : product_sale.Products.condition,
                'weight_gram' : product_sale.Products.weight_gram,
                'short_description' : product_sale.Products.short_description,
                'detail_product' : product_sale.Products.detail_product,
                'is_available' : product_sale.Products.is_available,
                'total_sold_qty': int(product_sale.total_sold_qty)
            }

            results.append(product_data)

        return results, 200


class ProductResource(Resource):
    def __init__(self):
        pass

    def get(self,id):
        product = Products.query.filter(Products.id==id).filter(Products.deleted==False).all()                   
        if product is not None:
            return marshal(product, Products.response_fields), 200
        else:
            return {'status': 'NOT FOUND'}, 404

api.add_resource(ProductList,'')
api.add_resource(ProductResource, '/<id>')   

