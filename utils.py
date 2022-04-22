from models import Cliente, Usuarios, OrdemServico

def insere():
    #pessoa = Pessoas(nome="Thiago",idade=30)
    #pessoa.save()
   # programador = Programador(nome="RAFAEL")
   # programador.save()
    #habilidade = Habilidade(nome="Back End")
    #habilidade.save()

    prog_hab = Programador_Habilidade(idprogramador=1,idhabilidade=1);
    prog_hab.save()
    
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
    
def insere_ordem(idcliente,titulo,descricao,idusuariocriacao):
    ordem = OrdemServico(idcliente=idcliente,titulo=titulo,descricao=descricao,idusuariocriacao=idusuariocriacao)
    ordem.save()

def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)

if __name__ == "__main__":
    #insere_cliente("RAFAEL SABOIA SILVA")
    #insere_usuario("rafaelsaboia","ubatuba")
    #insere_ordem(1,"teste","teste",1)
    #exclui_cliente(1)
    #consulta()