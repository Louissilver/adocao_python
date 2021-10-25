def solicitacao_adocaoEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "id_associado": item["id_associado"],
        "id_ong": item["id_ong"],
        "id_pet": item["id_pet"],
        "aprovado": item["aprovado"],
        "finalizado": item["finalizado"],
        "referencias": item["referencias"],
        "dataSolicitacao": item["dataSolicitacao"],
    }


def solicitacoes_adocaoEntity(entity) -> list:
    return [solicitacao_adocaoEntity(item) for item in entity]
