import json
from . import reset_db, app, client,  create_token



class TestRentCrud():

    idRent = 0
################################################################################################3
# RENT

    def test_rent_insert_internal(self, client):
        token = create_token(True)
        data = {
            "book_id":5,
            "user_id":2
        }

        res = client.post('/rent', json=data, headers={'Authorization': 'Bearer '+ token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id'] > 0       
        #self.idUser = res_json['id']


    # def test_rent_insert_noninternal(self, client):
    #     token = create_token()
    #     data = {
    #         "book_id":1,
    #         "user_id":1
    #     }

    #     res = client.post('/rent', json=data, headers={'Authorization': 'Bearer '+ token})
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 403


    ##### GET PUT DELETE BY ID
    def test_rent_list_internal(self, client):
        token = create_token(True)
        res = client.get('/rent/list', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
    

    def test_rent_get_id_internal(self, client):
        token = create_token(True)

        res = client.get('/rent/1', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_rent_update_internal(self, client):
        token = create_token(True)

        data = {
            "book_id": 4,
            "user_id": 2
        }


        res = client.put('/rent/1', json=data, headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
    


    def test_rent_delete_internal(self, client):
        token = create_token(True)


        res = client.delete('/rent/1', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['message'] == 'Deleted'