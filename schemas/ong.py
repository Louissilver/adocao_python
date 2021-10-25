def ongEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "nome": item["nome"],
        "email": item["email"],
        "telefone": item["telefone"],
        "endereco": item["endereco"],
        "cnpj": item["cnpj"],
        "id_pessoa": item["id_pessoa"],
    }


def ongsEntity(entity) -> list:
    return [ongEntity(item) for item in entity]
