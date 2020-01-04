from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from ..user.model import Users
from blueprints import admin_required

import json,hashlib

bp_auth = Blueprint('the_auth', __name__)
api = Api(bp_auth)


##  RESOURCE  ###

class CreateTokenResource(Resource):
    
    def post(self):
        ## CreateToken
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', location='json',required=True)
        parser.add_argument('the_password', location='json', required=True)
        args = parser.parse_args()

        
        password_digest = hashlib.md5(args['the_password'].encode()).hexdigest()
        qry = Users.query.filter_by(user_name=args['user_name']).filter_by(the_password=password_digest)
        userData = qry.first()

        if userData is not None:
            userData = marshal(userData, Users.jwt_claims_fields)
            token = create_access_token(identity=args['user_name'], user_claims=userData)

            #setelah token berhasil dibuat, info ke react utk simpan token, 
            #halaman bisa tetap di terakhir yg diakses atau gampangnya diarahkan ke home
            return {'token' : token}, 200
            
        else:
            return {'status': 'UNATUTHORIZED', 'message': 'invalid username or password'}, 401


class RefreshTokenResource(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity=current_user)
        return {'token': token}, 200

api.add_resource(CreateTokenResource,'')   
api.add_resource(RefreshTokenResource,'','/refresh')   
