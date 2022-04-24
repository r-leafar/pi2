from flask_restful import Resource
from pi2.models import Usuarios
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask import request

class LoginResource(Resource):
    def post(self):
        login = request.json.get("login", None)
        senha = request.json.get("senha", None)
        usuario = Usuarios.query.filter_by(login=login).first()
        
        if usuario:
            if check_password_hash(usuario.senha,senha):
                access_token = create_access_token(identity=login)
                return {"access_token":access_token}           

        return {"msg": "Bad username or password"}, 401
