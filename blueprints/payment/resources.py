from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from datetime import timedelta
import datetime

from blueprints import db, app
from .model import Payments
from blueprints.sale.model import Sales
from blueprints.bank_account.model import BankAccounts

from flask_jwt_extended import jwt_required

bp_payment = Blueprint('the_payment', __name__)  
api = Api(bp_payment)

    

class PaymentResource(Resource):

    @jwt_required
    def post(self, sale_id):
        #LAKUKAN PENGECEKAN UTK MEMASTIKAN DATA ORDERAN LENGKAP
        #SEMENTARA BELUM DIBUAT, NUNGGU DARI FRONT END PERILAKUNYA SPT APA
        #SALAH SATUNYA CEK APAKAH SEMUA SALE_DETAIL SUDAH DIINPUT ALAMAT PENGIRIMAN
        #APAKAH TERJADI UPDATE SALE_DETAILS (QTY, DISKON, ONGKIR DLL)

        payment = Payments.query.filter_by(sale_id=sale_id).first()

        if payment is None:
            parser = reqparse.RequestParser()
            parser.add_argument('bank_account_id', location='json',required=True)
            args = parser.parse_args() 

            bank_account_id = args['bank_account_id']

            sale = Sales.query.get(sale_id)
            total_to_transfer = sale.total_bill + (int(sale_id) % 1000)

            # d = datetime.datetime.today() + timedelta(days=days_to_calculate)
            expired_time = datetime.datetime.now() + timedelta(days=1)
            url_proof_img = ''

            new_payment = Payments(sale_id, bank_account_id, total_to_transfer, expired_time, url_proof_img)
            db.session.add(new_payment)

            db.session.commit()

            result = {}
            bank_info = BankAccounts.query.get(bank_account_id)
            result['payment'] = marshal(new_payment, Payments.response_fields)
            result['bank_info'] = marshal(bank_info, BankAccounts.payment_info_fields)

            return marshal(new_payment, Payments.response_fields), 200, {'Content Type':'application/json'}
        
        return marshal(payment, Payments.response_fields), 200, {'Content Type':'application/json'}
        
        # SEMENTARA DIDISABLE DULU KARENA HASIL RESPONSE BERBEDA
        # else:
        #     #cek expired time nya jika sudah lewat, maka buat lagi data baru dengan exp_time yg baru
        #     payment = Payments.query.filter(Payments.sale_id==sale_id).filter(Payments.expired_time > datetime.datetime.now()).first()

        #     if payment is None:

        #         parser = reqparse.RequestParser()
        #         parser.add_argument('bank_account_id', location='json',required=True)
        #         args = parser.parse_args() 

        #         bank_account_id = args['bank_account_id']

        #         sale = Sales.query.get(sale_id)
        #         total_to_transfer = sale.total_bill + (int(sale_id) % 1000)

        #         # d = datetime.datetime.today() + timedelta(days=days_to_calculate)
        #         expired_time = datetime.datetime.now() + timedelta(days=1)

        #         #args['expired_time'] berformat 'yyyy-mm-dd HH:mm:ss'
        #         # expired_time =  datetime.datetime.strptime(args['expired_time'], '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d %H%M%S')

        #         url_proof_img = ''

        #         new_payment = Payments(sale_id, bank_account_id, total_to_transfer, expired_time, url_proof_img)
        #         db.session.add(new_payment)

        #         db.session.commit()

        #         result = {}
        #         bank_info = BankAccounts.query.get(bank_account_id)
        #         result['payment'] = marshal(payment, Payments.response_fields)
        #         result['bank_info'] = marshal(bank_info, BankAccounts.payment_info_fields)

        #         return result, 200, {'Content Type':'application/json'}
        #     else:
        #         parser = reqparse.RequestParser()
        #         parser.add_argument('bank_account_id', location='json',required=True)
        #         args = parser.parse_args() 

        #         bank_account_id = args['bank_account_id']
        #         payment.bank_account_id = bank_account_id
        #         db.session.commit()

        #         result = {}
        #         bank_info = BankAccounts.query.get(bank_account_id)
        #         result['payment'] = marshal(payment, Payments.response_fields)
        #         result['bank_info'] = marshal(bank_info, BankAccounts.payment_info_fields)

        #         return result, 200, {'Content Type':'application/json'}




    @jwt_required
    def put(self, sale_id):

        parser = reqparse.RequestParser()
        #IMAGE BUKTI PEMBAYARAN DIUPLOAD OLEH USER, BERUPA FILE BINER DITAROH DI BODY 
        parser.add_argument('url_proof_img', location='json', required=True)
        args = parser.parse_args() 

        url_proof_img = args['url_proof_img']

        payment = Payments.query.filter(Payments.sale_id==sale_id).filter(Payments.expired_time > datetime.datetime.now()).first()
        if payment is not None:
            payment.url_proof_img = url_proof_img
            sale = Sales.query.get(sale_id)
            sale.is_paid = True
            db.session.commit()

            result = {}
            bank_info = BankAccounts.query.get(payment.bank_account_id)
            result['payment'] = marshal(payment, Payments.response_fields)
            result['bank_info'] = marshal(bank_info, BankAccounts.payment_info_fields)

            return result, 200, {'Content Type':'application/json'}
        
        return {'message': 'PAYMENT IS NOT FOUND'}, 404

api.add_resource(PaymentResource, '/<sale_id>')   