import json
from unittest import mock
from unittest.mock import patch
from . import client, test_login_admin, test_login_pembeli

from blueprints.shipping_address.resources import ItemShippingAddressResource

class TestMockRajaOngkir():
	def mocked_function_getCityId_call(city_name):
		if (city_name != None)and(len(city_name)>0):
			if city_name.lower() == 'malang':
				return 256
			else:
				return 23



	def mocked_requests_get(*args, **kwargs):
		class MockResponse:
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data

		if len(args) > 0:
			if args[0] == "https://api.rajaongkir.com/starter/cost":
				return MockResponse({
					"rajaongkir": {
						"results": [
							{
								"costs": [
									{
										"description": "Ongkos Kirim Ekonomis",
										"cost": [
											{
												"value": 17000,
											}
										]
									},
									{
										"description": "Layanan Reguler",
										"cost": [
											{
												"value": 20000,
											}
										]
									}
								]
							}
						]
					}			
				}, 200)
			elif args[0] == "https://api.rajaongkir.com/starter/city":
				return MockResponse({
                        "rajaongkir":{
                            "results": [
                                {
                                    "city_id": "256",
                                    "province_id": "11",
                                    "province": "Jawa Timur",
                                    "type": "Kota",
                                    "city_name": "Malang",
                                    "postal_code": "65112"
                                },
                                {
                                    "city_id": "257",
                                    "province_id": "16",
                                    "province": "Kalimantan Utara",
                                    "type": "Kabupaten",
                                    "city_name": "Malinau",
                                    "postal_code": "77511"
                                }]
                        }
				}, 200)
		else:
			return MockResponse(None, 404)



	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_function_GetCityId(self, test_reqget_mock, client):

		result = ItemShippingAddressResource.GetCityId(ItemShippingAddressResource, 'malang')

		assert result == 256
	
	@mock.patch('requests.get', side_effect=mocked_requests_get)
	# @mock.patch('ItemShippingAddressResource.GetCityId', side_effect=mocked_function_getCityId_call)
	# test_function_call
	def test_function_GetShippingFee(self, test_reqget_mock, client):

		result = ItemShippingAddressResource.GetShippingFee(ItemShippingAddressResource, 'malang', 'bandung', 1000)

		assert result == 20000