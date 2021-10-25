def usuarioEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "login": item["login"],
        "senha": item["senha"],
        "tipo_usuario": item["tipo_usuario"],
        "id_pessoa": item["id_pessoa"],
    }


def usuariosEntity(entity) -> list:
    return [usuarioEntity(item) for item in entity]
