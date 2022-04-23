from cProfile import run
from urllib import response
from flask import Flask, request
from flask_restful import Resource,Api
from models import Usuarios,Cliente,timedelta
from werkzeug.security import generate_password_hash,check_password_hash

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


class ClienteResource(Resource):
    # @auth.login_required
    def get(self,idcliente):
        cli = Cliente.query.filter_by(idcliente=idcliente).first()
        try:
            response ={
                "idcliente":cli.idcliente,
                "nome":cli.nome,
                "bairro":cli.bairro,
                "logradouro": cli.logradouro,
                "cidade":cli.cidade,
                "numero":cli.numero,
                "email":cli.email,
                "criadoem":(cli.criadoem- timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
                "alteradoem":(cli.alteradoem - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
                
            }
        except AttributeError:
            response ={
                "status":"error",
                "mensagem":"Cliente não encontrado"
            }
        return response

    def put(self,idcliente):
        cli = Cliente.query.filter_by(idcliente=idcliente).first()
        dados = request.json
        if "nome" in dados:
            cli.nome = dados["nome"]
        if "bairro" in dados:
            cli.bairro = dados["bairro"]
        if "logradouro" in dados:
            cli.logradouro = dados["logradouro"]
        if "cidade" in dados:
            cli.cidade = dados["cidade"]
        if "numero" in dados:
            cli.numero = dados["numero"]
        if "email" in dados:
            cli.email = dados["email"]
            
        cli.save()
        response ={
                "idcliente":cli.idcliente,
                "nome":cli.nome,
                "bairro":cli.bairro,
                "logradouro": cli.logradouro,
                "cidade":cli.cidade,
                "numero":cli.numero,
                "email":cli.email                
            }
        return response
    def delete(self,idcliente):
        cli = Cliente.query.filter_by(idcliente=idcliente).first()
        try:
            cli.delete()
            msg = "O cliente {} foi excluido com sucesso".format(cli.nome)
            status = "sucesso"
        except:
            msg = "Não foi possível excluir {}".format(cli.nome)
            status = "erro"
        return {
            "status":status,
            "mensagem":msg
        }

class ListarClienteResource(Resource):
    @jwt_required()
    def get(self):
        cli = Cliente.query.all()
        response = [ {"idcliente":i.idcliente,"nome":i.nome,"bairro":i.bairro,"logradouro":i.logradouro,"cidade":i.cidade,"numero":i.numero,"email":i.email,"criadoem":(i.criadoem- timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),"alteradoem":(i.alteradoem - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")} for i in cli]
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        return response
        
    def post(self):
        dados = request.json
        cli=Cliente(**dados)
        cli.save()
        return {
                "nome":cli.nome,
                "bairro":cli.bairro,
                "logradouro": cli.logradouro,
                "cidade":cli.cidade,
                "numero":cli.numero,
                "email":cli.email           
            }
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

        
        
api.add_resource(ClienteResource,"/cliente/<int:idcliente>")
api.add_resource(ListarClienteResource,"/cliente/")
api.add_resource(UsuarioResource,"/usuario/<int:idusuario>")
api.add_resource(ListarUsuarioResource,"/usuario/")
api.add_resource(LoginResource,"/login/")


if __name__ == "__main__":
        app.run(debug=True)