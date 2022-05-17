import asyncio
import json.decoder

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.python.classes.tables import Tables
from src.python.classes.users import Users
from src.python.exceptions.exceptions import ErrorCode
from src.python.services import encryption
from src.python.services.database import database as db
from src.python.services.response import json_response

user = APIRouter()

security = HTTPBasic()


@user.post("/create")
async def create(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "" or credentials.password == "":
        raise ErrorCode(401)

    try:
        body = await request.json()
    except json.decoder.JSONDecodeError:
        raise ErrorCode(400)

    if body.keys() != Users.required_keys():
        raise ErrorCode(400)

    password = encryption.gen_pbkdf2_sha256(credentials.password)

    new_user = Users(None, credentials.username, password, **body)

    asyncio.create_task(db.insert_value(Tables.USERS.value, new_user))

    return json_response({"user": new_user.response_format()}, 201)


@user.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    user_info = await db.print_from_param(Tables.USERS.value, ("LOGIN", credentials.username))

    if user_info is None:
        raise ErrorCode(404)

    temp_user = Users(*user_info)
    token, expiration_date = encryption.gen_access_token(str(temp_user.id))

    return json_response({"user": temp_user.response_format(),
                          "token_info": {
                              "token": token,
                              "expiration_date": expiration_date
                          }})
