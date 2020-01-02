from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
import datetime

from blueprints import db, app
from .model import ShippingAdresses
from blueprints.sale.model import Sales
from blueprints.sale_detail.model import SaleDetails
from blueprints.product.model import Products
from blueprints.merchant.model import MerchantProfiles

from flask_jwt_extended import jwt_required

import requests
import json

bp_item_shipping_address = Blueprint('item_shipping_address', __name__)  
api = Api(bp_item_shipping_address)



class ItemShippingAddressResource(Resource):

    RAJAONGKIR_API_KEY = '81f1cc4221bc944b6e665c72505e54a5'
    RAJAONGKIR_COST_API = 'https://api.rajaongkir.com/starter/cost'
    RAJAONGKIR_CITY_API = 'https://api.rajaongkir.com/starter/city'
    DEFAUT_COURIER = 'jne'

    def GetCityId(self, city_name):
        rq_city = requests.get(self.RAJAONGKIR_CITY_API, params={'key': self.RAJAONGKIR_API_KEY})
        result = rq_city.json()

        #city_list bertipe array
        city_list = result['rajaongkir']['results']
        for city in city_list:
            if city['city_name'].lower() == city_name.lower():
                return int(city['city_id'])


    def GetShippingFee(self, origin, destination, weight_gram):
        origin_id = self.GetCityId(origin)
        destination_id = self.GetCityId(destination)

        rq = requests.post(self.RAJAONGKIR_COST_API, json={'key': self.RAJAONGKIR_API_KEY, 'origin':origin_id, 'destination':destination_id, 'weight':weight_gram, 'courier':self.DEFAUT_COURIER})

        result = rq.json()

        #utk saat ini hanya memakai jasa kirim JNE saja, dan 
        # 1 tipe pengiriman yg ditentukan oleh perusahaan yaitu REGULER        
        #['costs'][1] berarti REGULER
        shipping_fee = result['rajaongkir']['results'][0]['costs'][1]['cost'][0]['value']
        # arrival_date_estimation = result['rajaongkir']['results'][0]['costs'][1]['cost'][0]['etd']

        
        return shipping_fee


    @jwt_required
    def get(self,sale_detail_id):
        item_shipping_address = ShippingAdresses.query.filter_by(sale_detail_id=sale_detail_id).first()
        if item_shipping_address is not None:
            return marshal(item_shipping_address, ShippingAdresses.response_fields), 200, {'Content Type':'application/json'}
        else:
            pass
        #panggil page berupa form utk mengisi alamat pengiriman item belanjaan
        #dan sediakan fitur berupa tombol utk mengisi otomatis alamat berdasarkan
        #alamat yg ada pada tabel user_profiles

    @jwt_required
    def post(self, sale_detail_id):
        parser = reqparse.RequestParser()
        parser.add_argument('address', location='json',required=True)
        parser.add_argument('district', location='json', required=True)
        parser.add_argument('city', location='json',required=True)
        parser.add_argument('province', location='json', required=True)
        parser.add_argument('postal_code', location='json')
        args = parser.parse_args() 

        address = args['address']
        district = args['district']
        city = args['city']
        province = args['province']
        if args['postal_code'] is None:
            postal_code = 0
        else:
            postal_code = int(args['postal_code'])

        new_item_shipping_address = ShippingAdresses(sale_detail_id, address, district, city, province, postal_code)
        db.session.add(new_item_shipping_address)


        #LAKUKAN KALKULASI ONGKIR DGN PANGGIL API PIHAK KE-3 RAJAONGKIR
        #UPDATE TOTAL BIAYA KIRIM DI TABEL sale_details total_shipping_fee
        sale_detail = SaleDetails.query.get(sale_detail_id)
        product = Products.query.get(sale_detail.product_id)
        merchant = MerchantProfiles.query.filter_by(user_id=product.merchant_id).first()
        merchant_city = merchant.city

        total_weight_gram = product.weight_gram * sale_detail.qty
        hasil = self.GetShippingFee(merchant_city, city, total_weight_gram)
        sale_detail.total_shipping_fee = hasil
        sale_detail.total = sale_detail.qty * sale_detail.price_on_sale - sale_detail.discount_amount + hasil

        # seharusnya proses update field total pd tabel sale_details
        # dan field total_bill pd tabel sales dilakukan dengan trigger
        # di project ini sementara dilakukan di backend framework nya
        # sale_detail.total = sale_detail.qty * sale_detail.price_on_sale - sale_detail.discount_amount + sale_detail.total_shipping_fee
        
        sale = Sales.query.get(sale_detail.sale_id)
        sale_details = SaleDetails.query.filter_by(sale_id=sale.id)
        total_bill = 0
        for each in sale_details:
            total_bill += each.total
        sale.total_bill = total_bill

        db.session.commit()

        return marshal(new_item_shipping_address, ShippingAdresses.response_fields), 200, {'Content Type':'application/json'}

    @jwt_required
    def put(self, sale_detail_id):

        parser = reqparse.RequestParser()
        parser.add_argument('address', location='json',required=True)
        parser.add_argument('district', location='json', required=True)
        parser.add_argument('city', location='json',required=True)
        parser.add_argument('province', location='json', required=True)
        parser.add_argument('postal_code', location='json')
        args = parser.parse_args() 

        item_shipping_address = ShippingAdresses.query.filter_by(sale_detail_id=sale_detail_id).first()
        if item_shipping_address is not None:

            address = args['address']
            district = args['district']
            city = args['city']
            province = args['province']
            if args['postal_code'] is None:
                postal_code = 0
            else:
                postal_code = int(args['postal_code'])

            item_shipping_address.address = address
            item_shipping_address.district = district
            item_shipping_address.city = city
            item_shipping_address.province = province
            item_shipping_address.postal_code = postal_code
            
            #LAKUKAN KALKULASI ONGKIR DGN PANGGIL API PIHAK KE-3 RAJAONGKIR
            #UPDATE TOTAL BIAYA KIRIM DI TABEL sale_details total_shipping_fee
            sale_detail = SaleDetails.query.get(sale_detail_id)
            product = Products.query.get(sale_detail.product_id)
            merchant = MerchantProfiles.query.filter_by(user_id=product.merchant_id).first()
            merchant_city = merchant.city

            total_weight_gram = product.weight_gram * sale_detail.qty
            hasil = self.GetShippingFee(merchant_city, city, total_weight_gram)
            sale_detail.total_shipping_fee = hasil
            sale_detail.total = sale_detail.qty * sale_detail.price_on_sale - sale_detail.discount_amount + hasil
            
            # seharusnya proses update field total pd tabel sale_details
            # dan field total_bill pd tabel sales dilakukan dengan trigger
            # di project ini sementara dilakukan di backend framework nya
            # sale_detail.total = sale_detail.qty * sale_detail.price_on_sale - sale_detail.discount_amount + sale_detail.total_shipping_fee
            
            sale = Sales.query.get(sale_detail.sale_id)
            sale_details = SaleDetails.query.filter_by(sale_id=sale.id)
            total_bill = 0
            for each in sale_details:
                total_bill += each.total
            sale.total_bill = total_bill

            
            db.session.commit()

            return marshal(item_shipping_address, ShippingAdresses.response_fields), 200, {'Content Type':'application/json'}

        return {'message': 'SHIPPING ADDRESS NOT FOUND'}, 404


api.add_resource(ItemShippingAddressResource, '/<sale_detail_id>')   