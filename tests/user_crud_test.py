import json
from . import reset_db, app, client,  test_login_admin, test_login_penjual, test_login_pembeli



class TestUserCrud():

    idUser = 0
    reset_db()

    def test_user_signup_regular_user(self, client):

        data = {
            "user_name" : "paijo123",
            "email" : "paijo@gmail..com",
            "the_password": "Paijo1234"
        }

        res = client.post('/user', json=data)

        res_json = json.loads(res.data)

        assert res.status_code == 200   

        self.idUser = res_json['id']


    def test_user_signup_regular_user_invalid_password(self, client):

        data = {
            "user_name" : "paijo1234",
            "email" : "paijoker@gmail.com",
            "the_password": "rahasia"
        }

        res = client.post('/user', json=data)

        res_json = json.loads(res.data)

        assert res.status_code == 400   
        assert res_json['message'] == 'password does not fill requirements'
        

    def test_user_signup_username_email_exist(self, client):

        data = {
            "user_name" : "admin",
            "email" : "paijo@gmail..com",
            "the_password": "Paijo1234"
        }

        res = client.post('/user', json=data)

        res_json = json.loads(res.data)

        assert res.status_code == 400   
        assert res_json['message'] == 'Username or Email already registered'
        

    def test_insert_new_user_profile_ganti_password_valid(self, client):
        token = test_login_admin()
        
        data = {
            "full_name" : "Saya adalah admin 1",
            "sex" : "male",
            "birth_place": "Semarang",
            "birth_date" : "1990-12-31",
            "phone_no" : "0361-798766",
            "address": "Jl. Merpati 23B",
            "city" : "Denpasar",
            "province" : "Bali",
            "bio": "Ini hanya sebuah user test",
            "url_img" : "https://cdn4.buysellads.net/uu/1/57095/1576856708-ad10.png",
            "password_changed" : True,
            "new_password": "NewPass1234"
        }

        res = client.put('/user/1', json=data,  headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
    

    def test_insert_new_user_profile_ganti_password_invalid(self, client):
        token = test_login_admin()
        
        data = {
            "full_name" : "Saya adalah admin 1",
            "sex" : "male",
            "birth_place": "Semarang",
            "birth_date" : "1990-12-31",
            "phone_no" : "0361-798766",
            "address": "Jl. Merpati 23B",
            "city" : "Denpasar",
            "province" : "Bali",
            "bio": "Ini hanya sebuah user test",
            "url_img" : "https://cdn4.buysellads.net/uu/1/57095/1576856708-ad10.png",
            "password_changed" : True,
            "new_password": "rahasia"
        }

        res = client.put('/user/1', json=data,  headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 400   
        assert res_json['message'] == 'password does not fill requirements'


    def test_update_user_profile_full(self, client):
        token = test_login_admin()
        
        data = {
            "full_name" : "Saya adalah admin 1",
            "sex" : "male",
            "birth_place": "Semarang",
            "birth_date" : "1990-12-31",
            "phone_no" : "0361-798766",
            "address": "Jl. Merpati 23B",
            "city" : "Denpasar",
            "province" : "Bali",
            "bio": "Ini hanya sebuah user test",
            "url_img" : "https://cdn4.buysellads.net/uu/1/57095/1576856708-ad10.png",
            "password_changed" : True,
            "new_password": "NewPass1234"
        }

        res = client.put('/user/1', json=data,  headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_update_user_profile_some_params_empty(self, client):
        token = test_login_admin()
        
        data = {
            "full_name" : "Saya adalah admin 1",
            "sex" : "male",
            "birth_date" : "1990-12-31",
            "phone_no" : "0361-798766",
            "password_changed" : False            
        }

        res = client.put('/user/1', json=data,  headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_update_user_profile_token_invalid(self, client):
        token = test_login_admin()
        
        data = {
            "full_name" : "Saya adalah admin 1",
            "sex" : "male",
            "birth_date" : "1990-12-31",
            "phone_no" : "0361-798766",
            "password_changed" : False            
        }

        res = client.put('/user/2', json=data,  headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 400
        assert res_json['message'] == 'Trying to Access/Update data by Unauthorized user'
    

    def test_get_user_by_id_token_valid(self, client):
        token = test_login_admin()
        
        res = client.get('/user/1', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_user_by_id_token_invalid(self, client):
        token = test_login_admin()

        res = client.get('/user/2', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 400
        assert res_json['message'] == 'Trying to Access/Update data by Unauthorized user'

    
        