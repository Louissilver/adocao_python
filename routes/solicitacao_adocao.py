from fastapi import APIRouter
from models.solicitacao_adocao import Solicitacao_Adocao
from fastapi import status

solicitacao_adocao = APIRouter()


@solicitacao_adocao.get('/adocao/solicitacoes', status_code=status.HTTP_200_OK)
async def find_all_solicitacoes_adocao():
    return Solicitacao_Adocao.retornar_solicitacoes()


@solicitacao_adocao.get('/adocao/solicitacoes/{id}', status_code=status.HTTP_200_OK)
async def find_one_solicitacao_adocao(id):
    return Solicitacao_Adocao.retornar_uma_solicitacao(id)


@solicitacao_adocao.post("/adocao/solicitacoes", status_code=status.HTTP_200_OK)
async def create_solicitacao_adocao(solicitacao_adocao: Solicitacao_Adocao):
    _id = solicitacao_adocao.inserir_solicitacao()
    id_solicitacao = _id.inserted_id
    return f"Solicitação de adoção {id_solicitacao} cadastrada com sucesso!"


@solicitacao_adocao.put('/adocao/solicitacoes/{id}', status_code=status.HTTP_200_OK)
async def update_solicitacao_adocao(id, solicitacao_adocao: Solicitacao_Adocao):
    solicitacao_adocao.atualizar_solicitacao(id)
    id_solicitacao = solicitacao_adocao.retornar_id_solicitacao(id)
    return f"Solicitação de adoção {id_solicitacao} alterada com sucesso!"


@solicitacao_adocao.put('/adocao/solicitacoes/aprovar/{id}', status_code=status.HTTP_200_OK)
async def aprovar_solicitacao_adocao(id):
    solicitacao = Solicitacao_Adocao.aprovar_solicitacao(id)
    return f"Solicitação {solicitacao} aprovada com sucesso!"


@solicitacao_adocao.put('/adocao/solicitacoes/finalizar/{id}', status_code=status.HTTP_200_OK)
async def finalizar_solicitacao_adocao(id):
    solicitacao = Solicitacao_Adocao.finalizar_solicitacao(id)
    return f"Solicitação {solicitacao} finalizada com sucesso!"


@solicitacao_adocao.delete('/adocao/solicitacoes/{id}', status_code=status.HTTP_200_OK)
async def delete_solicitacao_adocao(id):
    solicitacao_deletada = Solicitacao_Adocao.retornar_id_solicitacao(id)
    Solicitacao_Adocao.deletar_solicitacao(id)
    return f"A solicitação {solicitacao_deletada} foi excluída com sucesso!"
