import pytest, json, logging
from app import cache
from flask import Flask, request
from blueprints import db, app
from blueprints.user.model import Users
from blueprints.product_category.model import ProductCategories
from blueprints.bank_account.model import BankAccounts


#drop dan reset database
def reset_db():
    db.drop_all()
    db.create_all()

    #ketika unit test melakukan reset db dan membutuhkan inisialisasi data awal 
    #di beberapa tabel lakukan spt di bawah:
    #1 User admin, 1 user merchant, 1 user biasa (buyer)
    (self, user_name, email, the_password, is_admin, is_merchant):
    user_admin = Users("admin", "admin@gudangworkout.com", "Asdf1234", True, True)
    db.session.add(user_admin)
    user_seller = Users("penjual01", "budi@gmail.com", "Budi1234", False, True)
    db.session.add(user_seller)
    user_regular = Users("pembeli01", "susi@gmail.com", "Susi1234", False, False)
    db.session.add(user_regular)

    #2 ProductCategories
    prod_category1 = ProductCategories("Perlengkapan")
    db.session.add(prod_category1)
    prod_category2 = ProductCategories("Suplemen")
    db.session.add(prod_category2)
    prod_category3 = ProductCategories("Pakaian")
    db.session.add(prod_category3)

    #3 Bank Accounts
    (self, bank_name, account_name, account_no)
    bank1 = BankAccounts("BCA", "Djohn Dalton", "123-456-789-11")
    db.session.add(bank1)
    bank2 = BankAccounts("MANDIRI", "Widya Dewi", "987-654-321-01")
    db.session.add(bank2)
    
    db.session.commit()


def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture                        
def client(request):
    return call_client(request)     



def test_login_admin():

    cachename = 'test-admin-token'
    data = {
        'user_name': 'admin',
        'the_password': 'Asdf1234'
    }
    
    token = cache.get(cachename)

    if token is None:
        req = call_client(request)          
        res = req.post('/login', query_string=data)

        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        assert res.status_code == 200  

        cache.set('test-admin-token', res_json['token'], timeout=60)
        
        return res_json['token']

    else:
        return token

def test_login_penjual():

    cachename = 'test-penjual-token'
    data = {
        'user_name': 'penjual01',
        'the_password': 'Budi1234'
    }
    
    token = cache.get(cachename)

    if token is None:
        req = call_client(request)          
        res = req.post('/login', query_string=data)

        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        assert res.status_code == 200  

        cache.set('test-penjual-token', res_json['token'], timeout=60)
        
        return res_json['token']

    else:
        return token

def test_login_pembeli():

    cachename = 'test-pembeli-token'
    data = {
        'user_name': 'pembeli01',
        'the_password': 'Susi1234'
    }
    
    token = cache.get(cachename)

    if token is None:
        req = call_client(request)          
        res = req.post('/login', query_string=data)

        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        assert res.status_code == 200  

        cache.set('test-pembeli-token', res_json['token'], timeout=60)
        
        return res_json['token']

    else:
        return token