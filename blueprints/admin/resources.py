from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc, func
import datetime, hashlib


from blueprints import db, app, admin_required

from blueprints.user.model import Users
from blueprints.merchant.model import MerchantProfiles
from blueprints.product.model import Products
from blueprints.product_category.model import ProductCategories
from blueprints.bank_account.model import BankAccounts


from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from flask_jwt_extended import jwt_required
from password_strength import PasswordPolicy



bp_admin = Blueprint('the_admin', __name__)  
api = Api(bp_admin)

class ProductCategoryList(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('name', location='args')
        parser.add_argument('orderby', location='args', help='invalid orderby value')
        parser.add_argument('sort', location='args', help='invalid sort value')
        args = parser.parse_args()

        qry = ProductCategories.query.filter(ProductCategories.deleted==False)
         
        if args['name'] != None:
            qry = qry.filter(ProductCategories.name.like("%"+args['name']+"%"))

 
        indeks_mulai = (int(args['p']) * int(args['rp'])) - int(args['rp'])

        #sementara diurutkan hanya berdasarkan tanggal dibuat (terbaru)
        if args['orderby'] is not None:
            if args['orderby'] == 'created_at':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(ProductCategories.created_at))
                

        rows = []
        for row in qry.limit(int(args['rp'])).offset(indeks_mulai).all():
            rows.append(marshal(row, ProductCategories.response_fields))

        return rows, 200


class ProductCategoryNew(Resource):
    def __init__(self):
        pass

    @jwt_required
    @admin_required
    def post(self):        

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json',required=True)        
        args = parser.parse_args()

        name = args['name']
        category_is_exist = ProductCategories.query.filter(func.lower(ProductCategories.name) == name.lower()).first()
        if category_is_exist is None:
            new_category = ProductCategories(name)
            db.session.add(new_category)
            db.session.commit()

            return marshal(new_category, ProductCategories.response_fields), 200, {'Content Type':'application/json'}
        else:
            return {'message': 'Product Category is exist'}, 400, {'Content Type':'application/json'}


class ProductCategoryResource(Resource):
    def __init__(self):
        pass
    

    @jwt_required
    @admin_required
    def get(self,id):

        product_category = ProductCategories.query.filter(ProductCategories.deleted==False).filter(ProductCategories.id==id).first()                   
                    
        if product_category is not None:
            return marshal(product_category, ProductCategories.response_fields), 200
        else:
            return {'message': 'CATEGORY NOT FOUND'}, 404


    @jwt_required
    @admin_required
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json',required=True)        
        args = parser.parse_args()
        name = args['name']

        category_is_exist = ProductCategories.query.filter(ProductCategories.id != id).filter(func.lower(ProductCategories.name) == name.lower()).first()
        if category_is_exist is None:
            category = ProductCategories.query.get(id)
            category.name = name
            db.session.commit()

            return marshal(category, ProductCategories.response_fields), 200, {'Content Type':'application/json'}
        else:
            return {'message': 'Product Category is exist'}, 400, {'Content Type':'application/json'}

    @jwt_required
    @admin_required
    def delete(self, id):
        product_category = ProductCategories.query.get(id)
        if product_category is not None:
            products = Products.query.filter_by(category_id=id).all()
            for product in products:
                products.deleted = True

            
            product_category.deleted = True
            
            db.session.commit()
            
            return {'message': 'Deleted'}, 200
        else:
            return {'message': 'CATEGORY NOT FOUND'}, 404


class BankAccountList(Resource):
    def __init__(self):
        pass

    @jwt_required
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('bank_name', location='args')
        parser.add_argument('account_name', location='args')
        parser.add_argument('orderby', location='args', help='invalid orderby value')
        parser.add_argument('sort', location='args', help='invalid sort value')
        args = parser.parse_args()

        qry = BankAccounts.query.filter(BankAccounts.deleted==False)
         
        if args['bank_name'] != None:
            qry = qry.filter(BankAccounts.bank_name.like("%"+args['bank_name']+"%"))
        
        if args['account_name'] != None:
            qry = qry.filter(BankAccounts.account_name.like("%"+args['account_name']+"%"))
 
        indeks_mulai = (int(args['p']) * int(args['rp'])) - int(args['rp'])

        #sementara diurutkan hanya berdasarkan data terbaru dibuat
        if args['orderby'] is not None:
            if args['orderby'] == 'created_at':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(BankAccounts.created_at))

        rows = []
        for row in qry.limit(int(args['rp'])).offset(indeks_mulai).all():
            rows.append(marshal(row, BankAccounts.response_fields))

        return rows, 200



class BankAccountNew(Resource):
    def __init__(self):
        pass

    @jwt_required
    @admin_required
    def post(self):        
        
        parser = reqparse.RequestParser()
        parser.add_argument('bank_name', location='json',required=True)    
        parser.add_argument('account_name', location='json',required=True)        
        parser.add_argument('account_no', location='json',required=True)        
        args = parser.parse_args()

        bank_name = args['bank_name']
        account_name = args['account_name']
        account_no = args['account_no']

        bank_acc_is_exist = BankAccounts.query.filter(func.lower(BankAccounts.bank_name) == bank_name.lower()).first()
        # print(bank_acc_is_exist)
        if bank_acc_is_exist is None:    
            new_bank_account = BankAccounts(bank_name, account_name, account_no)
            db.session.add(new_bank_account)
            db.session.commit()

            return marshal(new_bank_account, BankAccounts.response_fields), 200, {'Content Type':'application/json'}
        else:
            return {'message': 'Bank Account is exist'}, 400, {'Content Type':'application/json'}


class BankAccountResource(Resource):
    def __init__(self):
        pass
        

    @jwt_required
    @admin_required
    def get(self,id):

        bank_account = BankAccounts.query.filter(BankAccounts.deleted==False).filter(BankAccounts.id==id).first()                   
                    
        if bank_account is not None:
            return marshal(bank_account, BankAccounts.response_fields), 200
        else:
            return {'message': 'BANK ACCOUNT NOT FOUND'}, 404

    @jwt_required
    @admin_required
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('bank_name', location='json',required=True)    
        parser.add_argument('account_name', location='json',required=True)        
        parser.add_argument('account_no', location='json',required=True)    
        args = parser.parse_args()

        bank_acc_is_exist = BankAccounts.query.filter(BankAccounts.id != id).filter(func.lower(BankAccounts.bank_name) == args['bank_name'].lower()).first()
        if bank_acc_is_exist is None: 
            bank_account = BankAccounts.query.get(id)
            bank_account.bank_name = args['bank_name']
            bank_account.account_name = args['account_name']
            bank_account.account_no = args['account_no']

            db.session.commit()

            return marshal(bank_account, BankAccounts.response_fields), 200, {'Content Type':'application/json'}
        else:
            return {'message': 'Bank Account is exist'}, 400, {'Content Type':'application/json'}


    @jwt_required
    @admin_required
    def delete(self, id):

        bank_account = BankAccounts.query.get(id)
        if bank_account != None:
            bank_account.deleted = True
            
            db.session.commit()
            
            return {'message': 'Deleted'}, 200
        else:
            return {'message': 'BANK ACCOUNT NOT FOUND'}, 404


api.add_resource(ProductCategoryList,'','/category')
api.add_resource(ProductCategoryNew,'','/category/new')
api.add_resource(ProductCategoryResource,'','/category/<id>')

api.add_resource(BankAccountList,'','/bank-account')
api.add_resource(BankAccountNew,'','/bank-account/new')
api.add_resource(BankAccountResource,'','/bank-account/<id>')


