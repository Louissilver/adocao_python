def associadoEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "nome": item["nome"],
        "email": item["email"],
        "telefone": item["telefone"],
        "endereco": item["endereco"],
        "cpf": item["cpf"],
        "dataNascimento": item["dataNascimento"],
        "animaisAdotados": item["animaisAdotados"],
        "id_pessoa": item["id_pessoa"],
    }


def associadosEntity(entity) -> list:
    return [associadoEntity(item) for item in entity]
