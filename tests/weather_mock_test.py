import json
from unittest import mock
from unittest.mock import patch
from . import client,  create_token

class TestMockWeatherBit():
	def mocked_requests_get(*args, **kwargs):
		class MockResponse:
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data

		if len(args) > 0:
			if args[0] == "https://api.weatherbit.io/v2.0/ip":
				return MockResponse({
					'city': 'Malang',
					'organization': 'ALTA',
					'timezone' : 'Asia/Jakarta',
					'latitude': 38,
					'longitude': -78.25,
						
				}, 200)
			elif args[0] == "https://api.weatherbit.io/v2.0/current":
				return MockResponse({
					'data':[{
						"datetime":"Jam Sepuluh Malam WIB",
						"temp":21.9
					}]
				}, 200)
		else:
			return MockResponse(None, 404)



	# @mock.patch('requests.get', side_effect=mocked_requests_get)
	# @mock.patch('requests.post', side_effect=mocked_requests_post)
	# def test_weather(self, test_reqpost_mock, test_reqget_mock):

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_weather(self, test_reqget_mock, client):
	# def test_weather(self, client):

		token = create_token(True)

		data = {
			'ip':'66.96.237.5'
		}

		resp = client.get('/weather/ip', query_string=data, headers={'Authorization': 'Bearer '+ token})
		
		json_data = json.loads(resp.data)


		assert resp.status_code == 200
		assert json_data['city'] == 'Malang'
		assert json_data['current_weather']['temp'] == 21.9