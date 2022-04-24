from flask_restful import Resource
from pi2.models import Cliente
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import timedelta

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