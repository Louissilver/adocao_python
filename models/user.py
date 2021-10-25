from pydantic import BaseModel

from config.db import conn
from schemas.user import userEntity, usersEntity
from bson import ObjectId


class User(BaseModel):
    name: str
    email: str
    password: str

    def retornarId(self, id):
        return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))

    def create_user(self):
        return conn.local.user.insert_one(dict(self))
