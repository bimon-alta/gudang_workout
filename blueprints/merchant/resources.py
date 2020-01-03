from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
import datetime, hashlib

from .model import MerchantProfiles
from blueprints import db, app
from blueprints.user.model import Users
from blueprints.product.model import Products
from blueprints.sale.model import Sales
from blueprints.sale_detail.model import SaleDetails


from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from flask_jwt_extended import jwt_required
from password_strength import PasswordPolicy



bp_merchant = Blueprint('the_merchant', __name__)  
api = Api(bp_merchant)


class MerchantNew(Resource):
    def get(self):
        pass
        #memanggil form utk register new merchant

    @jwt_required
    def post(self):
        verify_jwt_in_request()
        claims = get_jwt_claims()

        user = Users.query.filter_by(user_name=claims['user_name']).first()

        parser = reqparse.RequestParser()
        parser.add_argument('store_name', location='json',required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('district', location='json', required=True)
        parser.add_argument('city', location='json',required=True)
        parser.add_argument('province', location='json', required=True)
        parser.add_argument('postal_code', location='json')
        parser.add_argument('bank_name', location='json',required=True)
        parser.add_argument('bank_account_name', location='json', required=True)
        parser.add_argument('bank_account_no', location='json', required=True)

        args = parser.parse_args()

        user_id = user.id
        store_name = args['store_name']
        address = args['address']
        district = args['district']
        city = args['city']
        province = args['province']
        if args['postal_code'] is None:
            postal_code = 0
        else:
            postal_code = int(args['postal_code'])
        bank_name = args['bank_name']
        bank_account_name = args['bank_account_name']
        bank_account_no = args['bank_account_no']
        
        merchant_profile = MerchantProfiles(user_id, store_name, address, district, city, province, postal_code, bank_name, bank_account_name, bank_account_no )
        db.session.add(merchant_profile)
        #ubah stat is_merchant di table users
        user.is_merchant = True
        db.session.commit()

        #HARUS RETURN PROSES REDIRECT KE HALAMAN CRUD NEW PRODUCT
        return marshal(merchant_profile, MerchantProfiles.response_fields), 200, {'Content Type':'application/json'}



class MerchantResource(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self,id):
        merchant = MerchantProfiles.query.filter_by(user_id=id).first()

        if merchant is not None:
            return marshal(merchant, MerchantProfiles.response_fields), 200
        else:
            #ARAHKAN UTK REGISTRASI SEBAGAI MERCHANT
            #KE URL "/merchant"
            return {'message': 'MERCHANT NOT FOUND'}, 404


    
    @jwt_required
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('store_name', location='json',required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('district', location='json', required=True)
        parser.add_argument('city', location='json',required=True)
        parser.add_argument('province', location='json', required=True)
        parser.add_argument('postal_code', location='json')
        parser.add_argument('bank_name', location='json',required=True)
        parser.add_argument('bank_account_name', location='json', required=True)
        parser.add_argument('bank_account_no', location='json', required=True)

        args = parser.parse_args()

        store_name = args['store_name']
        address = args['address']
        district = args['district']
        city = args['city']
        province = args['province']
        if args['postal_code'] is None:
            postal_code = 0
        else:
            postal_code = int(args['postal_code'])
        bank_name = args['bank_name']
        bank_account_name = args['bank_account_name']
        bank_account_no = args['bank_account_no']
  
        merchant_profile = MerchantProfiles.query.filter_by(user_id=id).first()

        merchant_profile.store_name = store_name
        merchant_profile.address = address
        merchant_profile.district = district
        merchant_profile.city = city
        merchant_profile.province = province
        merchant_profile.postal_code = postal_code
        merchant_profile.bank_name = bank_name
        merchant_profile.bank_account_name = bank_account_name
        merchant_profile.bank_account_no = bank_account_no

        db.session.commit()

        return marshal(merchant_profile, MerchantProfiles.response_fields), 200, {'Content Type':'application/json'}

class MerchantProductList(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('category_id', location='args')
        parser.add_argument('orderby', location='args', help='invalid orderby value')
        parser.add_argument('sort', location='args', help='invalid sort value')
        args = parser.parse_args()


        verify_jwt_in_request()
        claims = get_jwt_claims()

        user = Users.query.filter_by(user_name=claims['user_name']).first()

        products = Products.query.filter(Products.deleted==False).filter(Products.merchant_id==user.id)
         

        if args['category_id'] != None:
            products = products.filter(Products.category_id==int(args['category_id']))

 
        indeks_mulai = (int(args['p']) * int(args['rp'])) - int(args['rp'])

        #sementara diurutkan hanya berdasarkan produk dibuat (terbaru/lama)
        if args['orderby'] is not None:
            if args['orderby'] == 'created_at':
                if args['sort'] == 'desc':
                    products = products.order_by(desc(Products.created_at))
                else:
                    products = products.order_by(Products.created_at)

        rows = []
        for row in products.limit(int(args['rp'])).offset(indeks_mulai).all():
            rows.append(marshal(row, Products.response_fields))

        return rows, 200
        


class MerchantCreateProduct(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    def get(self):
        #balikin form utk input product baru
        pass
    
    @jwt_required
    def post(self):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        user = Users.query.filter_by(user_name=claims['user_name']).first()

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json',required=True)
        parser.add_argument('category_id', location='json', required=True)
        parser.add_argument('default_price', location='json',required=True)
        parser.add_argument('brand_name', location='json', required=True)
        parser.add_argument('country_of_origin', location='json', required=True)
        parser.add_argument('url_img1', location='json',required=True)
        parser.add_argument('url_img2', location='json', required=True)
        parser.add_argument('url_img3', location='json', required=True)
        parser.add_argument('condition', location='json',required=True)
        parser.add_argument('weight_gram', location='json',required=True)
        parser.add_argument('short_description', location='json', required=True)
        parser.add_argument('detail_product', location='json', required=True)
        parser.add_argument('is_available', location='json', type=inputs.boolean, required=True)
        args = parser.parse_args()

        name = args['name']
        merchant_id = user.id
        category_id = args['category_id']
        default_price = args['default_price']
        brand_name = args['brand_name']
        country_of_origin = args['country_of_origin']
        url_img1 = args['url_img1']
        url_img2 = args['url_img2']
        url_img3 = args['url_img3']
        condition = args['condition']
        weight_gram = args['weight_gram']
        short_description = args['short_description']
        detail_product = args['detail_product']
        is_available = args['is_available']



        new_product = Products(name, merchant_id, category_id, default_price, brand_name, country_of_origin, url_img1, url_img2, url_img3, condition, weight_gram, short_description, detail_product, is_available)
        db.session.add(new_product)
        db.session.commit()


        #HARUS RETURN PROSES REDIRECT KE HALAMAN CRUD NEW PRODUCT
        return marshal(new_product, Products.response_fields), 200, {'Content Type':'application/json'}

class MerchantProductResource(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    def get(self,id):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        user = Users.query.filter_by(user_name=claims['user_name']).first()

        product = Products.query.filter(Products.deleted==False).filter(Products.merchant_id==user.id).filter(Products.id==id).first()                   
                    
        if product is not None:
            return marshal(product, Products.response_fields), 200
        else:
            return {'message': 'PRODUCT NOT FOUND'}, 404

    @jwt_required
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json',required=True)
        parser.add_argument('category_id', location='json', required=True)
        parser.add_argument('default_price', location='json',required=True)
        parser.add_argument('brand_name', location='json', required=True)
        parser.add_argument('country_of_origin', location='json', required=True)
        parser.add_argument('url_img1', location='json',required=True)
        parser.add_argument('url_img2', location='json', required=True)
        parser.add_argument('url_img3', location='json', required=True)
        parser.add_argument('condition', location='json',required=True)
        parser.add_argument('weight_gram', location='json',required=True)
        parser.add_argument('short_description', location='json', required=True)
        parser.add_argument('detail_product', location='json', required=True)
        parser.add_argument('is_available', location='json', type=inputs.boolean, required=True)
        args = parser.parse_args()


        product = Products.query.get(id)

        product.name = args['name']
        product.category_id = args['category_id']
        product.default_price = args['default_price']
        product.brand_name = args['brand_name']
        product.country_of_origin = args['country_of_origin']
        product.url_img1 = args['url_img1']
        product.url_img2 = args['url_img2']
        product.url_img3 = args['url_img3']
        product.condition = args['condition']
        product.weight_gram = args['weight_gram']
        product.short_description = args['short_description']
        product.detail_product = args['detail_product']
        product.is_available = args['is_available']
     
        db.session.commit()

        #HARUS RETURN PROSES REDIRECT KE HALAMAN CRUD NEW PRODUCT
        return marshal(product, Products.response_fields), 200, {'Content Type':'application/json'}

    @jwt_required
    def delete(self, id):
        product = Products.query.get(id)
        product.deleted = True        
        db.session.commit()
        
        return {'message': 'Deleted'}, 200

class MerchantOrderList(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    def get(self):

        verify_jwt_in_request()
        claims = get_jwt_claims()
        user = Users.query.filter_by(user_name=claims['user_name']).first()

        productsMerchant = Products.query.filter_by(deleted=False).filter_by(merchant_id=user.id).all()

        product_id_list = []
        for product in productsMerchant:
            product_id_list.append(product.id)

        # qry = qry.filter(Users.id.in_(users_id))

        # sale_details = db.session.query(Sales.is_paid,Sales.id, SaleDetails.id).join(SaleDetails).group_by(Products.id).filter(SaleDetails.is_shipped==False).filter(SaleDetails.product_id.in_(product_id_list))
        sale_details = SaleDetails.query.filter_by(is_shipped=False).filter(SaleDetails.product_id.in_(product_id_list)).order_by(SaleDetails.id).all()
       
        result = []
        for sale_detail in sale_details:
            item_list = {}
            product_info = Products.query.get(sale_detail.product_id)
            item_list['item_sale'] = marshal(sale_detail, SaleDetails.response_fields)
            item_list['item_info'] =  marshal(product_info, Products.order_list_field)
            result.append(item_list)

        return result, 200

api.add_resource(MerchantNew, '')
api.add_resource(MerchantResource, '/<id>')   
api.add_resource(MerchantProductList, '/product')
api.add_resource(MerchantCreateProduct, '/product/new')   
api.add_resource(MerchantProductResource, '/product/<id>')   
api.add_resource(MerchantOrderList, '/orders')   

