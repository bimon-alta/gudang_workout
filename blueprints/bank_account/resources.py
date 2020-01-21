from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc, func
import datetime

from .model import BankAccounts
from blueprints import db, app

from flask_jwt_extended import jwt_required

bp_bank_account = Blueprint('the_bank_account', __name__)  
api = Api(bp_bank_account)


    
class BankAccountList(Resource):
    def __init__(self):
        pass

    def get(self):

        bank_accounts = BankAccounts.query.filter_by(deleted=False).all()

        results = []
       
        for bank_account in bank_accounts:
            results.append(marshal(bank_account, BankAccounts.response_fields))

        return results, 200


class BankAccountResource(Resource):
    def __init__(self):
        pass

    def get(self,id):
        bank_account = BankAccounts.query.filter(BankAccounts.id==id).filter(BankAccounts.deleted==False).all()                   
        if bank_account is not None:
            return marshal(product, BankAccounts.response_fields), 200
        else:
            return {'status': 'NOT FOUND'}, 404

api.add_resource(BankAccountList,'')
api.add_resource(BankAccountResource,'/<id>')


