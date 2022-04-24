from cProfile import run
from urllib import response
from flask import Flask, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from pi2.resources.clienteresource import ClienteResource
from pi2.resources.listarclienteresource import ListarClienteResource
from pi2.resources.usuarioresource import UsuarioResource
from pi2.resources.listarusuarioresource import ListarUsuarioResource
from pi2.resources.loginresource import LoginResource

app = Flask(__name__)
api = Api(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
    
api.add_resource(ClienteResource,"/cliente/<int:idcliente>")
api.add_resource(ListarClienteResource,"/cliente/")
api.add_resource(UsuarioResource,"/usuario/<int:idusuario>")
api.add_resource(ListarUsuarioResource,"/usuario/")
api.add_resource(LoginResource,"/login/")


if __name__ == "__main__":
        app.run(debug=True)