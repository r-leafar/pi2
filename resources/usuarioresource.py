from flask_restful import Resource
from werkzeug.security import generate_password_hash
from pi2.models import Usuarios
from datetime import timedelta

class UsuarioResource(Resource):
    def get(self,idusuario):
        usuario = Usuarios.query.filter_by(idusuario=idusuario).first()
        return {
            "idusuario":usuario.idusuario,
            "login":usuario.login,
            "senha": usuario.senha,
            "criadoem":(usuario.criadoem- timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
            "alteradoem":(usuario.alteradoem - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
        }
    def put(self,idusuario):
        usuario = Usuarios.query.filter_by(idusuario=idusuario).first()
        dados = request.json
        if "login" in dados:
            usuario.login = dados["login"]
        if "senha" in dados:
            usuario.senha = generate_password_hash(dados["senha"])
        usuario.save()
        response ={
                "idusuario":usuario.idusuario,
                "login":usuario.login,
                "senha":usuario.senha
                }
        return response
        
    def delete(self,idusuario):
        usuario = Usuarios.query.filter_by(idusuario=idusuario).first()
        try:
            usuario.delete()
            msg = "O usuario {} foi excluido com sucesso".format(usuario.login)
            status = "sucesso"
        except:
            msg = "Não foi possível excluir {}".format(usuario.login)
            status = "erro"
        
        return {
            "status":status,
            "mensagem":msg
        }