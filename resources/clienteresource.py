from flask_restful import Resource
from pi2.models import Cliente
from datetime import timedelta
from flask import request

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
