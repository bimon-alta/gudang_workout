import json
from . import reset_db, app, client,  test_login_admin, test_login_pembeli



class TestAdminCRUD():

    reset_db()

    def test_product_category_insert_new(self, client):
        token = test_login_admin()

        data = { "name" : "peralatan"}
        res = client.post('/admin/category/new', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200   

    def test_product_category_insert_new_already_exist(self, client):
        token = test_login_admin()

        data = { "name" : "Suplemen"}
        res = client.post('/admin/category/new', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 400    
        assert res_json['message'] == 'Product Category is exist'

    def test_product_category_get_by_id(self, client):
        token = test_login_admin()

        res = client.get('/admin/category/1')
        res_json = json.loads(res.data)
        assert res.status_code == 200  


    def test_product_category_get_by_id_not_found(self, client):
        token = test_login_admin()

        res = client.get('/admin/category/99')
        res_json = json.loads(res.data)
        assert res.status_code == 404  
        assert res_json['message'] == 'CATEGORY NOT FOUND'

    def test_product_category_update_by_id(self, client):
        token = test_login_admin()

        data = { "name" : "Lain-lain"}
        res = client.put('/admin/category/1', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200  

    def test_product_category_update_by_id_name_is_exist(self, client):
        token = test_login_admin()

        data = { "name" : "Suplemen"}
        res = client.put('/admin/category/1', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 400
        assert res_json['message'] == 'Product Category is exist'  

    def test_product_category_delete_by_id(self, client):
        token = test_login_admin()

        res = client.delete('/admin/category/1', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200 

    def test_product_category_delete_by_id_notfound(self, client):
        token = test_login_admin()

        res = client.delete('/admin/category/999', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 404 
        assert res_json['message'] == 'CATEGORY NOT FOUND'

#===================================== BANK ACCOUNT ===========================================

    def test_bank_account_insert_new(self, client):
        token = test_login_admin()

        data = { 
            "bank_name" : "Bank Jateng",
            "account_name" : "Soewarni Soesilo",
            "account_no" : "971-909-6566-9991",
        }
        res = client.post('/admin/bank-account/new', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200   

    def test_bank_account_insert_new_already_exist(self, client):
        token = test_login_admin()

        data = { 
            "bank_name" : "BCA",
            "account_name" : "Soewarni Soesilo",
            "account_no" : "971-909-6566-9991",
        }
        res = client.post('/admin/bank-account/new', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 400    
        assert res_json['message'] == 'Bank Account is exist'

    def test_bank_account_get_by_id(self, client):
        token = test_login_admin()

        res = client.get('/admin/bank-account/1')
        res_json = json.loads(res.data)
        assert res.status_code == 200  


    def test_bank_account_get_by_id_not_found(self, client):
        token = test_login_admin()

        res = client.get('/admin/bank-account/999')
        res_json = json.loads(res.data)
        assert res.status_code == 404  
        assert res_json['message'] == 'BANK ACCOUNT NOT FOUND'

    def test_bank_account_update_by_id(self, client):
        token = test_login_admin()

        data = { 
            "bank_name" : "BCA",
            "account_name" : "Soewarni Soesilo",
            "account_no" : "971-909-6566-9991",
        }
        res = client.put('/admin/bank-account/1', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200  

    def test_bank_account_update_by_id_name_is_exist(self, client):
        token = test_login_admin()

        data = { 
            "bank_name" : "MANDIRI",
            "account_name" : "Soewarni Soesilo",
            "account_no" : "971-909-6566-9991",
        }
        res = client.put('/admin/bank-account/1', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 400
        assert res_json['message'] == 'Bank Account is exist'  

    def test_bank_account_delete_by_id(self, client):
        token = test_login_admin()

        res = client.delete('/admin/bank-account/1', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200 

    def test_bank_account_delete_by_id_notfound(self, client):
        token = test_login_admin()

        res = client.delete('/admin/bank-account/999', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 404 
        assert res_json['message'] == 'BANK ACCOUNT NOT FOUND'

    def test_bank_account_get_all_list(self, client):
        token = test_login_admin()

        data = { 
            "bank_name" : "BCA",
            "account_name" : "Soewarni Soesilo",
            "orderby" : "created_at",
            "sort" : "desc",
        }
        res = client.get('/admin/bank-account', args=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200    
