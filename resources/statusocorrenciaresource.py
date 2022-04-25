from flask_restful import Resource
from flask import request
from pi2.models import StatusOcorrencia
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import timedelta

class StatusOcorrenciaResource(Resource):
    def get(self,idstatus):
        status = StatusOcorrencia.query.filter_by(idstatus=idstatus).first()
        return {
            "idstatus":status.idstatus,
            "nome":status.nome,
            "criadoem":(status.criadoem- timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
            "alteradoem":(status.alteradoem - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
        }
    def put(self,idstatus):
        status = StatusOcorrencia.query.filter_by(idstatus=idstatus).first()
        dados = request.json
        if "nome" in dados:
            status.nome = dados["nome"]
        status.save()
        response ={
                "idstatus":status.idstatus,
                "nome":status.nome
                }
        return response

    def delete(self,idstatus):
        status = StatusOcorrencia.query.filter_by(idstatus=idstatus).first()
        try:
            status.delete()
            msg = "O status [{}] foi excluido com sucesso".format(status.nome)
            st = "sucesso"
        except:
            msg = "Não foi possível excluir [{}]".format(status.nome)
            st = "erro"
        
        return {
            "status":st,
            "mensagem":msg
        }