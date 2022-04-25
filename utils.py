from models import Cliente, Usuarios, OrdemServico,StatusOcorrencia

def insere_status():
    status = StatusOcorrencia(nome="ENCAMINHADO P/ USUARIO")
    status.save()

def consulta():
    prog_hab = Programador_Habilidade.query.all()
    for p in prog_hab:
        print(p.programador.nome+" "+p.habilidade.nome)

def exclui_cliente(idcliente):
    cli = Cliente.query.filter_by(idcliente=idcliente).first()
    cli.delete()
    
def insere_usuario(login,senha):
    usuario = Usuarios(login=login,senha=senha)
    usuario.save()

def insere_cliente(nome):
    cli = Cliente(nome=nome)
    cli.save()
    
def insere_ordem(idcliente,titulo,descricao,idusuariocriacao,idstatus):
    ordem = OrdemServico(idcliente=idcliente,titulo=titulo,descricao=descricao,idusuariocriacao=idusuariocriacao,idstatus=idstatus)
    ordem.save()

def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)

if __name__ == "__main__":
    insere_cliente("RAFAEL SABOIA SILVA")
    insere_usuario("rafaelsaboia","pbkdf2:sha256:260000$dKGUN77BhkjwSoiz$e21a94efb49544cc4177c2581d3e4ff9f5809ef19177ad94b62d25cdf9f8e526")
    insere_status()
    insere_ordem(1,"teste","teste",1,1)
    #exclui_cliente(1)
    #consulta()