import json
from . import reset_db, app, client,  create_token



class TestBookCrud():

    idBook = 0
    pass


################################################################################################3
# BOOK
    ############# POST 

    def test_book_insert_internal(self, client):
        token = create_token(True)
        data = {
            "title": "Judul Buku 14",
            "isbn": "1-234-5678-9101112-19",
            "writer": "Dr. John"
        }

        res = client.post('/book', json=data, headers={'Authorization': 'Bearer '+ token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id'] > 0       
        
       #self.idUser = res_json['id']


    # def test_book_insert_noninternal(self, client):
    #     token = create_token()
    #     data = {
            # "title": "Judul Buku 7",
            # "isbn": "1-234-5678-9101112-18",
            # "writer": "Dr. John"
    #     }

        # res = client.post('/book', json=data, headers={'Authorization': 'Bearer '+ token})
        # res_json = json.loads(res.data)
        # assert res.status_code == 403


        # res = client.put('/user/1', json=data, headers={'Authorization': 'Bearer '+ token})

        # res_json = json.loads(res.data)
        # assert res.status_code == 200

    ##### GET PUT DELETE BY ID
    def test_book_list_internal(self, client):
        token = create_token(True)
        res = client.get('/book/list', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
    

    def test_book_get_id_internal(self, client):
        token = create_token(True)

        res = client.get('/book/1', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_book_update_internal(self, client):
        token = create_token(True)

        data = {
            "title": "Judul Buku 1",
            "isbn": "1-234-5678-9101112-18",
            "writer": "Dr. John"
        }


        res = client.put('/book/1', json=data, headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
    


    def test_book_delete_internal(self, client):
        token = create_token(True)


        res = client.delete('/book/1', headers={'Authorization': 'Bearer '+ token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['message'] == 'Deleted'

    