from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi import status
from models.associado import Associado
from models.pessoa import Pessoa
from models.usuario import Usuario

associado = APIRouter()


@associado.get('/associados', status_code=status.HTTP_200_OK)
async def find_all_associados():
    return Associado.retornar_associados()


@associado.get('/associados/{id}', status_code=status.HTTP_200_OK)
async def find_one_associado(id):
    return Associado.retornar_um_associado(id)


@associado.post("/associados", status_code=status.HTTP_200_OK)
async def create_associado(associado: Associado, usuario: Usuario):
    if associado.email in Associado.retornar_emails_existentes():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="O e-mail informado já está em uso.")
    _id_pessoa = associado.inserir_pessoa()
    id_pessoa = str(_id_pessoa.inserted_id)

    _id_associado = associado.inserir_associado()
    id_associado = str(_id_associado.inserted_id)

    usuario.tipo_usuario = "Associado"
    if usuario.login in Usuario.retornar_logins_existentes():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="O login informado já está em uso.")
    _id_usuario = usuario.inserir_usuario()
    id_usuario = str(_id_usuario.inserted_id)

    associado.inserir_id_pessoa(id_associado, id_pessoa)
    usuario.inserir_id_pessoa(id_usuario, id_pessoa)

    return f"O associado {associado.nome} foi inserido com sucesso!"


@associado.put('/associados/{id}', status_code=status.HTTP_200_OK)
async def update_associado(id, associado: Associado):
    if associado.email in Pessoa.retornar_emails_existentes(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="O e-mail informado já está em uso.")
    associado.atualizar_associado(id)
    return f"O associado {associado.nome} foi alterado com sucesso!"


@associado.delete('/associados/{id}', status_code=status.HTTP_200_OK)
async def delete_associado(id):
    associado = Associado.retornar_nome_associado(id)
    id_pessoa = Associado.retornar_id_pessoa(id)
    Usuario.deletar_usuario(id_pessoa)
    Pessoa.deletar_pessoa(id_pessoa)
    Associado.deletar_associado(id)
    return f"O associado {associado} foi excluido com sucesso!"
