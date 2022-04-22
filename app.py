from cProfile import run
from urllib import response
from flask import Flask, request
from flask_restful import Resource,Api
from models import Pessoas,Atividades,Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

# USUARIOS = {
#     "rafael":"123",
#     "silvio":"321"

# }
@auth.verify_password
def verificacao(login,senha):
    if not (login,senha):
        return False
    return Usuarios.query.filter_by(login=login,senha=senha).first()

class Cliente(Resource):
    @auth.login_required
    def get(self,idcliente):
        cli = Cliente.query.filter_by(idcliente=idcliente).first()
        try:
            response ={
                "idcliente":cli.id,
                "nome":cli.nome,
                "bairro":cli.bairro,
                "logradouro": cli.logradouro,
                "cidade":cli.cidade,
                "numero":cli.numero,
                "email":cli.email,
                "criadoem":cli.criadoem
                
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
                "idcliente":cli.id,
                "nome":cli.nome,
                "bairro":cli.bairro,
                "logradouro": cli.logradouro,
                "cidade":cli.cidade,
                "numero":cli.numero,
                "email":cli.email                
            }
        return response
    def delete(self,idcliente):
        pessoa = Pessoas.query.filter_by(idcliente=idcliente).first()
        pessoa.delete()
        msg = "O {} foi excluido com sucesso".format(pessoa.nome)
        return {
            "status":"sucesso",
            "mensagem":msg
        }
class ListarPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [ {"id":i.id,"nome":i.nome,"idade":i.idade} for i in pessoas]
        return response
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados["nome"],idade=dados["idade"])
        pessoa.save()
        return {
            "id":pessoa.id,
            "nome": pessoa.nome,
            "idade":pessoa.idade

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

api.add_resource(Pessoa,"/pessoa/<string:nome>")
api.add_resource(ListarPessoas,"/pessoa/")
api.add_resource(ListarAtividades,"/atividade/")

if __name__ == "__main__":
        app.run(debug=True)