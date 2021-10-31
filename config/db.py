from pymongo import MongoClient, collection

conn = MongoClient()

db = conn.adocao

associado = db["associado"]
ong = db["ong"]
pessoa = db["pessoa"]
usuario = db["usuario"]
pet = db["pet"]
solicitacao_adocao = db["solicitacao_adocao"]

associado.create_index("cpf", unique=True)
ong.create_index("cnpj", unique=True)
pessoa.create_index("email", unique=True)
usuario.create_index("login", unique=True)
