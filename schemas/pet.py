def petEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "nome": item["nome"],
        "especie": item["especie"],
        "raca": item["raca"],
        "dataNascimento": item["dataNascimento"],
        "sexo": item["sexo"],
        "porte": item["porte"],
        "adotado": item["adotado"],
        "urlFoto": item["urlFoto"],
        "observacoes": item["observacoes"],
    }


def petsEntity(entity) -> list:
    return [petEntity(item) for item in entity]
