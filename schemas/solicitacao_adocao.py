def solicitacao_adocaoEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "id_associado": item["id_associado"],
        "id_ong": item["id_ong"],
        "id_pet": item["id_pet"],
        "nome_pet": item["nome_pet"],
        "nome_ong": item["nome_ong"],
        "cnpj_ong": item["cnpj_ong"],
        "email_ong": item["email_ong"],
        "telefone_ong": item["telefone_ong"],
        "nome_associado": item["nome_associado"],
        "cpf_associado": item["cpf_associado"],
        "telefone_associado": item["telefone_associado"],
        "email_associado": item["email_associado"],
        "aprovado": item["aprovado"],
        "finalizado": item["finalizado"],
        "referencias": item["referencias"],
        "dataSolicitacao": item["dataSolicitacao"],
    }


def solicitacoes_adocaoEntity(entity) -> list:
    return [solicitacao_adocaoEntity(item) for item in entity]
