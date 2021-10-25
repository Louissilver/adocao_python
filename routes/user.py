from fastapi import APIRouter

from models.user import User
from config.db import conn
from schemas.user import userEntity, usersEntity
from bson import ObjectId

user = APIRouter()


@user.get('/')
async def find_all_users():
    return usersEntity(conn.local.user.find())


@user.get('/{id}')
async def find_one_user(id):
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))


@user.post('/', response_description="Usuário cadastrado com sucesso", status_code=200)
async def create_user(user: User):
    _id = user.create_user()
    id = str(_id.inserted_id)
    return user.retornarId(id)


@ user.put('/{id}')
async def update_user(id, user: User):
    conn.local.user.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))


@ user.delete('/{id}')
async def delete_user(id):
    return userEntity(conn.local.user.find_one_and_delete({"_id": ObjectId(id)}))
