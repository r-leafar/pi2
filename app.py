from cProfile import run
from urllib import response
from flask import Flask, request
from flask_restful import Resource,Api
from models import Usuarios,Cliente,timedelta
#from flask_httpauth import HTTPBasicAuth

#auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

# USUARIOS = {
#     "rafael":"123",
#     "silvio":"321"

# }
#@auth.verify_password
def verificacao(login,senha):
    if not (login,senha):
        return False
    return Usuarios.query.filter_by(login=login,senha=senha).first()

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
        cli.delete()
        msg = "O cliente {} foi excluido com sucesso".format(cli.nome)
        return {
            "status":"sucesso",
            "mensagem":msg
        }
class ListarClienteResource(Resource):
    def get(self):
        cli = Cliente.query.all()
        response = [ {"idcliente":i.idcliente,"nome":i.nome,"bairro":i.bairro,"logradouro":i.logradouro,"cidade":i.cidade,"numero":i.numero,"email":i.email,"criadoem":(i.criadoem- timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),"alteradoem":(i.alteradoem - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")} for i in cli]
        return response,200
    def post(self):
        dados = request.json
        #cli = Cliente(nome=dados["nome"],bairro=dados["bairro"],
        #logradouro=dados["logradouro"],cidade=dados["cidade"],numero=dados["numero"],email=dados["email"])
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
class ListarAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{"id":i.id,"nome":i.nome,"pessoa":i.pessoa.nome} for i in atividades]
        return response
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados["pessoa"]).first()
        atividade = Atividades(nome=dados["nome"],pessoa=pessoa)
        atividade.save()

api.add_resource(ClienteResource,"/cliente/<int:idcliente>")
api.add_resource(ListarClienteResource,"/cliente/")


if __name__ == "__main__":
        app.run(debug=True)