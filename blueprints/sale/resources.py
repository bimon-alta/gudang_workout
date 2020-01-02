from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
import datetime

from blueprints import db, app
from .model import Sales
from blueprints.sale_detail.model import SaleDetails
from blueprints.user.model import Users

from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims

bp_sale = Blueprint('the_sale', __name__)  
api = Api(bp_sale)
    
    

class SaleResource(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        user = Users.query.filter_by(user_name=claims['user_name']).first()
        
        cart = Sales.query.filter_by(user_id=user.id).first()
        cart_items = SaleDetails.query.filter_by(sale_id=cart.id).all()

        cart_item_list = []
        if cart_items is not None:
            for cart_item in cart_items:
                cart_item_list.append(marshal(cart_items, SaleDetails.response_fields))

        result = {
            'sale': marshal(cart, Sales.response_fields),
            'sale_detail': cart_item_list
        }

        return result, 200

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json',required=True)
        parser.add_argument('qty', location='json', required=True)
        parser.add_argument('price_on_sale', location='json',required=True)
        parser.add_argument('discount_amount', location='json', required=True)
        # parser.add_argument('total_shipping_fee', location='json', required=True)
        # parser.add_argument('total', location='json',required=True)
        # parser.add_argument('is_shipped', location='json', required=True)
        args = parser.parse_args()

        product_id = args['product_id']
        qty = int(args['qty'])
        price_on_sale = int(args['price_on_sale'])
        discount_amount = int(args['discount_amount'])
        # total_shipping_fee = args['total_shipping_fee']
        total = qty * price_on_sale - discount_amount
        # is_shipped = args['is_shipped']

        verify_jwt_in_request()
        claims = get_jwt_claims()
        user = Users.query.filter_by(user_name=claims['user_name']).first()
        cart = Sales.query.filter_by(user_id=user.id).first()

        if cart is None:
            new_cart = Sales(user.id, total, False)
            db.session.add(new_cart)
            db.session.commit()

            cart = Sales.query.filter_by(user_id=user.id).first()
            new_item = SaleDetails(cart.id, product_id, qty, price_on_sale, discount_amount, 0, total,False)
            db.session.add(new_item)
            db.session.commit()

            return marshal(new_item, SaleDetails.response_fields), 200, {'Content Type':'application/json'}

        else:
            cart = Sales.query.filter_by(user_id=user.id).first()
            item = SaleDetails.query.filter_by(product_id=product_id).first()
            if item is None:
                new_item = SaleDetails(cart.id, product_id, qty, price_on_sale, discount_amount, 0, total,False)
                db.session.add(new_item)

                cart.total_bill += total
                db.session.commit()

                return marshal(new_item, SaleDetails.response_fields), 200, {'Content Type':'application/json'}

            else:
                item.qty += 1
                item.total += total 

            
                cart.total_bill += total
                db.session.commit()

                return marshal(item, SaleDetails.response_fields), 200, {'Content Type':'application/json'}


    @jwt_required
    def delete(self):
        pass

api.add_resource(SaleResource,'')  


