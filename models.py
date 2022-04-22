from sqlalchemy import create_engine,Column,Integer,String,DateTime,Boolean,ForeignKey,PrimaryKeyConstraint
from sqlalchemy.orm import scoped_session,sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime


engine = create_engine("sqlite:///pi2.db",encoding="utf8")
db_session = scoped_session(sessionmaker(autocommit=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class OrdemServico(Base):
    __tablename__="ordem_servico"
    idordemservico = Column(Integer,primary_key=True)
    idcliente = Column(Integer,ForeignKey("cliente.idcliente"),nullable=False)
    titulo = Column(String(40),nullable=False)
    descricao = Column(String(250),nullable=False)
    idusuariocriacao = Column(Integer,ForeignKey("usuarios.idusuario"),nullable=False)
    criadoem = Column(DateTime,default = datetime.datetime.utcnow,nullable=False)
    alteradoem = Column(DateTime,onupdate = datetime.datetime.utcnow,default = datetime.datetime.utcnow,nullable=False)
    usuario = relationship("Usuarios",cascade="all,delete",backref="ordemservico_usuario")
    cliente = relationship("Cliente",cascade="all,delete",backref="ordemservico_cliente")
    
    
    def __repr__(self):
        return "<Ordem Servico {}>".format(self.nome)
    def save(self):
        db_session.add(self)
        db_session.commit()
    def delete(self):
        db_session.delete(self)
        db_session.commit()
    

class Cliente(Base):
    __tablename__="cliente"
    idcliente = Column(Integer,primary_key=True)
    nome = Column  (String(80),nullable=False)
    bairro = Column  (String(80))
    logradouro=Column  (String(100))
    cidade =Column  (String(100))
    numero = Column  (String(80))
    email = Column  (String(80))
    criadoem = Column(DateTime,default = datetime.datetime.utcnow,nullable=False)
    ativo =  Column(Boolean, default=True,nullable=False)

    def __repr__(self):
        return "<Cliente {}>".format(self.nome)
    def save(self):
        db_session.add(self)
        db_session.commit()
    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Assentamento(Base):
    __tablename__="assentamento"
    idassentamento = Column(Integer,primary_key=True)
    idcliente = Column(Integer,ForeignKey("cliente.idcliente"),nullable=False)
    idusuariocriacao = Column(Integer,ForeignKey("usuarios.idusuario"),nullable=False)
    idordemservico = Column(Integer,ForeignKey("ordem_servico.idordemservico"),nullable=False)
    descricao = Column  (String(250))
    criadoem = Column(DateTime,default = datetime.datetime.utcnow,nullable=False)
    cliente = relationship("Cliente",cascade="all,delete",backref="assentamento_cliente")
    usuario = relationship("Usuarios",cascade="all,delete",backref="assentamento_usuario")
    
    def __repr__(self):
        return "<Assentamento {}>".format(self.nome)
    def save(self):
        db_session.add(self)
        db_session.commit()
    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Usuarios(Base):
    __tablename__="usuarios"
    idusuario = Column(Integer,primary_key=True)
    login = Column(String(20),unique=True)
    senha = Column(String(20))
    criadoem = Column(DateTime,default = datetime.datetime.utcnow,nullable=False)
    ativo =  Column(Boolean, default=True,nullable=False)

    def __repr__(self) -> str:
        return "<Usuario {}>".format(self.login)
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    def delete(self):
        db_session.delete(self)
        db_session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)
    
if __name__ == "__main__":
    init_db()
