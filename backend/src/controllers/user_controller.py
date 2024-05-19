from flask import request, Response, json, Blueprint
from src import bcrypt, db
from src.models.user_model import User
from src.services.jwt_service import generate_jwt

users = Blueprint("users", __name__)

@users.route('/signup', methods = ["POST"])
def handle_signup():
    try: 
        data = request.json
        if "firstname" in data and "lastname" and data and "email" and "password" in data:
            user = User.query.filter_by(email = data["email"]).first()
            if not user:
                user_obj = User(
                    firstname = data["firstname"],
                    lastname = data["lastname"],
                    email = data["email"],
                    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                )
                db.session.add(user_obj)
                db.session.commit()

                token = generate_jwt(user_obj)
                return Response(
                    response=json.dumps({'status': "success", "message": "User Sign up Successful", "token": token}),
                    status=201,
                    mimetype='application/json'
                )
            else:
                return Response(
                    response=json.dumps({'status': "failed", "message": "User already exists"}),
                    status=409,
                    mimetype='application/json'
                )
        else:
            return Response(
                response=json.dumps({'status': "failed", "message": "User Parameters Firstname, Lastname, Email and Password are required"}),
                status=400,
                mimetype='application/json'
            )
        
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error Occured", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )

@users.route('/login', methods = ["POST"])
def handle_login():
    try: 
        data = request.json
        if "email" and "password" in data:
            user = User.query.filter_by(email = data["email"]).first()

            if user:
                if bcrypt.check_password_hash(user.password, data["password"]):
                    token = generate_jwt(user)
                    return Response(
                        response = json.dumps({'status': "success", "message": "User Sign In Successful", "token": token}),
                        status=200,
                        mimetype='application/json'
                    )
                
                else:
                    return Response(
                        response = json.dumps({'status': "failed", "message": "User Password Mistmatched"}),
                        status = 401,
                        mimetype = 'application/json'
                    ) 
            else:
                return Response(
                    response = json.dumps({'status': "failed", "message": "User Record doesn't exist, kindly register"}),
                    status = 404,
                    mimetype = 'application/json'
                ) 
        else:
            return Response(
                response = json.dumps({'status': "failed", "message": "User Parameters Email and Password are required"}),
                status = 400,
                mimetype ='application/json'
            )
        
    except Exception as e:
        return Response(
            response = json.dumps({'status': "failed", "message": "Error Occured", "error": str(e)}),
            status = 500,
            mimetype = 'application/json'
        )