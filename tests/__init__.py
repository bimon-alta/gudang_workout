import pytest, json, logging
from app import cache
from flask import Flask, request
from blueprints import db, app
from blueprints.client.model import Clients

#drop dan reset database
def reset_db():
    db.drop_all()
    db.create_all()

    #ketika unit test melakukan reset db dan membutuhkan inisialisasi data awal 
    #di beberapa tabel lakukan spt di bawah:
    client = Clients("internal", "asdf1234", 'true')
    db.session.add(client)
    client = Clients("non internal", "asdf1234", 'false')
    db.session.add(client)
    db.session.commit()


#diakali dibuat fungsi call_client agar tidak masalah dgn fixture
def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture                         #biar bisa dipanggil di semua fungsi test
def client(request):
    return call_client(request)     

#fungsi 'client' di atas tidak dipakai di dalam file ini, hanya bisa dipakai di file lain


def create_token(isAdmin=False):

    #prepare request input, untuk sementara sesuaikan dgn data di db
    if isInternal:
        cachename = 'test-admin-token'
        data = {
            'user_name': 'admin',
            'the_password': 'Asdf1234'
        }
    else:
        cachename = 'test-nonadmin-token'
        data = {
            'user_name': 'Shopper1',
            'the_password': 'User1234'
        }
        

    # ambil token dari cache
    token = cache.get(cachename)

    if token is None:
        #do request
        #diakali dibuat fungsi call_client agar tidak masalah dgn fixture
        req = call_client(request)          
        res = req.get('/token', query_string=data)

        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        #output dari test (ukuran keberhasilan pengetesan)
        #proses pengetesan berhasil hanya jika mengembalikan response/status code 200
        assert res.status_code == 200  

        #menyimpan kembali token ke cache
        cache.set('test-internal-token', res_json['token'], timeout=60)
        
        return res_json['token']

    else:
        #kembalikan token jika tak ada cache
        return token

