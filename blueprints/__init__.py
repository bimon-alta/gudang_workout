
#app.py

import json, os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager                    #UTK menjalankan migration nya
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps

app = Flask(__name__)     

##################################
# JWT
##################################

app.config['JWT_SECRET_KEY'] = 'tHISisMySecretK3y'
app.config['JWT_ACCESS_TOKEN_EXPRESS'] = timedelta(days=1)

jwt = JWTManager(app)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'status': 'FORBIDDEN', 'message': 'Admin Only'}, 403
        else:
            return fn(*args, **kwargs)

    return wrapper

##################################


app.config['APP_DEBUG'] = True


##################################
# DATABASE
##################################

#sqlalchemy config
# try:
#     env = os.environ.get('FLASK_ENV', 'development')
#     if env == 'testing':
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/gudang_workout_db_testing'
#     else:
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/gudang_workout_db'

# except Exception as e:
#     raise e

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/gudang_workout_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)                #inisialisasi sqlalchemy

migrate = Migrate(app, db)          #inisialisasi migrate nya

manager = Manager(app)              #inisialisasi manager

manager.add_command('db', MigrateCommand)           #fungsi utk menjalankan migrasi

##################################





################################
# MIDDLEWARE
################################

################## LOG FEATURE ###########################
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()


        if response.status_code == 200:
            app.logger.info("REQUEST_LOG\t%s",  
                json.dumps({
                    'status_code': response.status_code,
                    'method': request.method,
                    'code': response.status,
                    'uri': request.full_path,
                    'request': requestData,
                    'response': json.loads(response.data.decode('utf-8'))
                }))   
        else:
            app.logger.error("REQUEST_LOG\t%s", 
                json.dumps({
                    'status_code': response.status_code,
                    'method': request.method,
                    'code': response.status,
                    'uri': request.full_path,
                    'request': requestData,
                    'response': json.loads(response.data.decode('utf-8'))
                }))   

    return response



######################################
# Import blueprints
######################################
from blueprints.home.resources import bp_home
from blueprints.auth import bp_auth
from blueprints.user.resources import bp_user
from blueprints.merchant.resources import bp_merchant 
from blueprints.admin.resources import bp_admin
from blueprints.product.resources import bp_product
from blueprints.sale.resources import bp_sale
from blueprints.shipping_address.resources import bp_item_shipping_address
from blueprints.payment.resources import bp_payment


# from blueprints.weather import bp_weather

app.register_blueprint(bp_home,url_prefix='/')
app.register_blueprint(bp_auth, url_prefix='/login')
app.register_blueprint(bp_user,url_prefix='/user')
app.register_blueprint(bp_merchant,url_prefix='/merchant')
app.register_blueprint(bp_admin,url_prefix='/admin')
app.register_blueprint(bp_product,url_prefix='/product')
app.register_blueprint(bp_sale,url_prefix='/cart')
app.register_blueprint(bp_item_shipping_address,url_prefix='/shipping-address')
app.register_blueprint(bp_payment,url_prefix='/payment')


# app.register_blueprint(bp_weather, url_prefix='/weather')

db.create_all()
