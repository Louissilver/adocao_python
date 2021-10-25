def pessoaEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "nome": item["nome"],
        "email": item["email"],
        "telefone": item["telefone"],
        "endereco": item["endereco"]
    }


def pessoasEntity(entity) -> list:
    return [pessoaEntity(item) for item in entity]
