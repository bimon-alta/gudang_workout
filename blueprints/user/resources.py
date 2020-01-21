from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc, or_, func
import datetime, hashlib

from .model import Users
from blueprints import db, app, admin_required
from blueprints.user_profile.model import UserProfiles

from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from password_strength import PasswordPolicy



bp_user = Blueprint('the_user', __name__)  
api = Api(bp_user)




class UserResource(Resource):
    def __init__(self):
        pass
    
    def patch(self):
        pass
        #memanggil form utk register new user


    @jwt_required
    def get(self,id):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        get_user_from_token = Users.query.filter_by(user_name=claims['user_name']).first()

        if get_user_from_token.id == int(id):
            # user = Users.query.get(id)            
            return marshal(get_user_from_token, Users.response_fields), 200
        else:
            #IDENTITAS TOKEN DAN ID PARAMS TIDAK MATCH
            return {'message': 'Trying to Access/Update data by Unauthorized user'}, 400, {'Content Type':'application/json'}


    def post(self):
        policy = PasswordPolicy.from_names(
            length = 8,
            uppercase = 1,
            numbers = 1
            # special = 2
        )

        parser = reqparse.RequestParser()
        parser.add_argument('user_name', location='json',required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('the_password', location='json', required=True)
        args = parser.parse_args()
        
        user_name = args['user_name']
        email = args['email'].lower()

        validation = policy.test(args['the_password'])
        
        if validation == []:
            user_is_exist = Users.query.filter(or_(Users.user_name==user_name, Users.email==email)).first()
            if user_is_exist is None:
                password_digest = hashlib.md5(args['the_password'].encode()).hexdigest()
                user = Users(user_name, email, password_digest, False, False)
                db.session.add(user)
                db.session.commit()

                #PROSES RETURN HARUSNYA MENGEMBALIKAN PROSES UTK REDIRECT KE API PEMBUATAN TOKEN
                #DARI API PEMBUATAN TOKEN JIKA BERHASIL LANGSUNG DIARAHKAN KE HOME PAGE
                return {'result': marshal(user, Users.response_fields)}, 200, {'Content Type':'application/json'}
            else:
                # print('USERNAME EMAIL ADAAAA')
                return {'message': 'Username or Email already registered'}, 400, {'Content Type':'application/json'}
                
        else:
            return {'message': 'password does not fill requirements'}, 400, {'Content Type':'application/json'}



    @jwt_required
    def put(self, id):
        verify_jwt_in_request()
        claims = get_jwt_claims()

        get_user_from_token = Users.query.filter_by(user_name=claims['user_name']).first()

        if get_user_from_token.id == int(id):
            policy = PasswordPolicy.from_names(
                length = 8,
                uppercase = 1,
                numbers = 1
                # special = 2
            )

            parser = reqparse.RequestParser()

            parser.add_argument('full_name', location='json',required=True)
            parser.add_argument('sex', location='json', required=True)
            parser.add_argument('birth_place', location='json')
            parser.add_argument('birth_date', location='json', required=True)
            parser.add_argument('phone_no', location='json', required=True)
            parser.add_argument('address', location='json')
            parser.add_argument('city', location='json')
            parser.add_argument('province', location='json')
            parser.add_argument('bio', location='json')
            parser.add_argument('url_img', location='json')
            parser.add_argument('password_changed', type=inputs.boolean, location='json', required=True)
            parser.add_argument('new_password', location='json')

            args = parser.parse_args()

            if args['password_changed'] == True:
                validation = policy.test(args['new_password'])
                if validation == []:
                    # user = Users.query.get(id)
                    password_digest = hashlib.md5(args['new_password'].encode()).hexdigest()
                    get_user_from_token.the_password = password_digest
                else:
                    return {'message': 'password does not fill requirements'}, 400, {'Content Type':'application/json'}

            

            full_name = args['full_name']
            sex = args['sex']
            if args['birth_place'] is None:
                birth_place = ''
            else:
                birth_place = args['birth_place']
            
            #args['birth_date'] berformat yyyy-mm-dd
            birth_date =  datetime.datetime.strptime(args['birth_date'], '%Y-%m-%d').strftime('%Y%m%d')
            
            phone_no = args['phone_no']
            if args['address'] is None:
                address = ''
            else:
                address = args['address']

            if args['city'] is None:
                city = ''
            else:
                city = args['city']

            if args['province'] is None:
                province = ''
            else:
                province = args['province']
            
            if args['bio'] is None:
                bio = ''
            else:
                bio = args['bio']

            if args['url_img'] is None:
                url_img = ''
            else:
                url_img = args['url_img']
            

            

            # user = Users.query.get(id)
            user_profile = UserProfiles.query.filter_by(user_id=int(id)).first()

            if user_profile is None:
                user_profile = UserProfiles(get_user_from_token.id, full_name, sex, birth_place, birth_date, phone_no, address, city, province, bio, url_img)
                db.session.add(user_profile)
                db.session.commit()

                return marshal(user_profile, UserProfiles.response_fields), 200, {'Content Type':'application/json'}
            else:
                user_profile = UserProfiles.query.filter_by(user_id=int(id)).first()
                user_profile.full_name = full_name
                user_profile.sex = sex
                user_profile.birth_place = birth_place
                user_profile.birth_date = birth_date
                user_profile.phone_no = phone_no
                user_profile.address = address
                user_profile.city = city
                user_profile.province = province
                user_profile.bio = bio
                user_profile.url_img = url_img
                db.session.commit()

                return marshal(user_profile, UserProfiles.response_fields), 200, {'Content Type':'application/json'}
    
        else:
            #IDENTITAS TOKEN DAN ID PARAMS TIDAK MATCH
            return {'message': 'Trying to Access/Update data by Unauthorized user'}, 400, {'Content Type':'application/json'}
        
api.add_resource(UserResource,'','/<id>')   

