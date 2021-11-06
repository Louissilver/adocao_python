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
        "id_ong": item["id_ong"],
    }


def petsEntity(entity) -> list:
    return [petEntity(item) for item in entity]
