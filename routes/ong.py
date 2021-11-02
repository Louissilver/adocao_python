from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi import status
from models.ong import Ong
from models.pessoa import Pessoa
from models.usuario import Usuario

ong = APIRouter()


@ong.get('/ongs', status_code=status.HTTP_200_OK)
async def find_all_ongs():
    return Ong.retornar_ongs()


@ong.get('/ongs/{id}', status_code=status.HTTP_200_OK)
async def find_one_ong(id):
    return Ong.retornar_uma_ong(id)


@ong.post("/ongs", status_code=status.HTTP_200_OK)
async def create_ong(ong: Ong, usuario: Usuario):
    if ong.email in Ong.retornar_emails_existentes():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="O e-mail informado já está em uso.")
    if ong.cnpj in Ong.retornar_cnpjs_existentes():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="O CNPJ informado já está em uso.")
    if usuario.login in Usuario.retornar_logins_existentes():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="O login informado já está em uso.")
    _id_pessoa = ong.inserir_pessoa()
    id_pessoa = str(_id_pessoa.inserted_id)

    _id_ong = ong.inserir_ong()
    id_ong = str(_id_ong.inserted_id)

    usuario.tipo_usuario = "ONG"
    usuario.senha = Usuario.get_passwordhash(usuario.senha)
    _id_usuario = usuario.inserir_usuario()
    id_usuario = str(_id_usuario.inserted_id)

    ong.inserir_id_pessoa(id_ong, id_pessoa)
    usuario.inserir_id_pessoa(id_usuario, id_pessoa)

    return f"ONG {ong.nome} inserida com sucesso!"


@ong.put('/ongs/{id}', status_code=status.HTTP_200_OK)
async def update_ong(id, ong: Ong):
    if ong.email in Ong.retornar_emails_existentes(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="O e-mail informado já está em uso.")
    if ong.cnpj in Ong.retornar_cnpjs_existentes(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="O CNPJ informado já está em uso.")
    ong.atualizar_ong(id)
    return f"A ONG {ong.nome} foi alterada com sucesso!"


@ong.delete('/ongs/{id}', status_code=status.HTTP_200_OK)
async def delete_ong(id):
    ong = Ong.retornar_nome_ong(id)
    id_pessoa = Ong.retornar_id_pessoa(id)
    Usuario.deletar_usuario(id_pessoa)
    Pessoa.deletar_pessoa(id_pessoa)
    Ong.deletar_ong(id)
    return f"A ONG {ong} foi excluida com sucesso!"
