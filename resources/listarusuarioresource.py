from flask_restful import Resource
from pi2.models import Usuarios
from datetime import timedelta

class ListarUsuarioResource(Resource):
    def get(self):
        usuarios = Usuarios.query.all()
        response = [ {"idusuario":i.idusuario,"login":i.login,"criadoem":(i.criadoem- timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),"alteradoem":(i.alteradoem - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")} for i in usuarios]
        return response
        
    def post(self):
        dados = request.json
        usuario=Usuarios(**dados)
        usuario.senha = generate_password_hash(dados["senha"])
        usuario.save()
        return {
                "login":usuario.login,
                "senha":usuario.senha
            }