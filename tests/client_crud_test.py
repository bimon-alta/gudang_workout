import json
from . import reset_db, app, client,  create_token



class TestClientCrud():

    idClient = 0


################################################################################################3
# CLIENT

    def test_client_insert_internal(self, client):
        token = create_token(True)
        data = {
            'client_key' : 'admin14',
            'client_secret' : 'asdf1234',
            'status' : 'false'
        }

        res = client.post('/client', json=data, headers={'Authorization': 'Bearer '+ token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['client_id'] > 0     

        # self.idUser = res_json['id']


    # def test_client_insert_noninternal(self, client):
    #     token = create_token()
    #     data = {
    #         'client_key' : 'non admin',
    #         'client_secret' : 'asdf1234',
    #         'status' : 'false'
    #     }

    #     res = client.post('/client', json=data, headers={'Authorization': 'Bearer '+ token})
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 403

    ##### GET PUT DELETE BY ID
    def test_client_list_internal(self, client):
        token = create_token(True)

        data = {
            'p' : 1,
            'rp': 10,
            'status': True,
            'orderby': 'status',
            'sort': 'asc'
        }
        res = client.get('/client/list', query_string=data, headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
    

    def test_client_get_id_internal(self, client):
        token = create_token(True)

        res = client.get('/client/6', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_client_update_internal(self, client):
        token = create_token(True)

        data = {
            "client_key": "client_ext",
            "client_secret": "asdf1234",
            "status": "false"
        }


        res = client.put('/client/6', json=data, headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
    


    def test_client_delete_internal(self, client):
        token = create_token(True)


        res = client.delete('/client/6', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['message'] == 'Deleted'

    