import json
from unittest import mock
from unittest.mock import patch
from . import client, test_login_admin, test_login_pembeli

from blueprints.shipping_address.resources import ItemShippingAddressResource

class TestMockRajaOngkir():
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
				}, 200)
		else:
			return MockResponse(None, 404)



	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_function_GetCityId(self, test_reqget_mock, client):

		result = ItemShippingAddressResource.GetCityId('malang')

		assert result == 256
	
	def test_function_GetShippingFee(self, test_reqget_mock, client):

		result = ItemShippingAddressResource.GetShippingFee(256, 23, 1000)

		assert result == 20000