from flask_restful import Resource
from pi2.models import StatusOcorrencia
from datetime import timedelta
from flask import request


class  ListarStatusOcorrenciaResource(Resource):
    def get(self):
        status = StatusOcorrencia.query.all()
        response = [ {"idstatus":i.idstatus,"nome":i.nome,"criadoem":(i.criadoem- timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),"alteradoem":(i.alteradoem - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")} for i in status]
        # Access the identity of the current user with get_jwt_identity
        return response

    def post(self):
        dados = request.json
        status=StatusOcorrencia(**dados)
        status.save()
        return {
                "nome":status.nome
            }