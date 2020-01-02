import json
from . import reset_db, app, client,  create_token



class TestUserCrud():

    idUser = 0
    # reset_db()

    def test_user_insert_internal(self, client):
        token = create_token(True)

        data = {
            "name" : "John Constantine3",
            "age" : 20,
            "sex": "male",
            "client_id" : 1
        }

        res = client.post('/user', json=data, headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)

        #output dari test (ukuran keberhasilan pengetesan)
        assert res.status_code == 200   #hanya jika mengembalikan status code 200 dan id > 0, dianggap ok 
        # assert res_json['id'] > 0       

        #jika mau mengetest juga apakah metode validasi 'client_secret' sukses
        # assert res_json['client_secret'] == hashlib.md5(args['client_secret'].encode()).hexdigest()

        self.idUser = res_json['id']





    # def test_user_insert_noninternal(self, client):
    #     token = create_token()

    #     data = {
    #         "name" : "Bimon1",
    #         "age" : 20,
    #         "sex": "male",
    #         "client_id" : 1
    #     }


    #     res = client.post('/user', json=data, headers={'Authorization': 'Bearer '+ token})

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 403
    #     # assert res_json['validate'][0] == 'at least 1 uppercase'  #ini validasi password, tidak dipakai


    #     # self.idUser = res_json['id']

    

    def test_user_list_internal(self, client):
        token = create_token(True)
        res = client.get('/user/list', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # def test_user_list_noninternal(self, client):
    #     token = create_token()
    #     res = client.get('/user/list', headers={'Authorization': 'Bearer '+ token})

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 500

    # def test_user_list_without_token(self, client):
    #     token = create_token()
    #     data = {
    #         "p" : 1,
    #         "rp" : 20,
    #         "name": "Bimon",
    #         "ordery": "age",
    #         "sort" : "desc"
    #     }

    #     res = client.get('/user/list', query_string=data, headers={'Authorization': 'Bearer '})

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 500

    def test_user_update_internal(self, client):
        token = create_token(True)

        data = {
            "name" : "Christine",
            "age" : 18,
            "sex": "female",
            "client_id" : 2
        }


        res = client.put('/user/2', json=data, headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_user_delete_internal(self, client):
        token = create_token(True)

        res = client.delete('/user/2', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['message'] == 'Deleted'


    def test_user_get_id_internal(self, client):
        token = create_token(True)

        res = client.get('/user/2', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
    


