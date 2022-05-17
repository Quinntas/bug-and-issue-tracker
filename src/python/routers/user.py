import asyncio

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.python.classes.tables import Tables
from src.python.classes.users import Users
from src.python.services import encryption
from src.python.services.database import database as db
from src.python.services.response import json_response

user = APIRouter()

security = HTTPBasic()


@user.post("/create")
async def create(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    body = await request.json()
    password = encryption.gen_pbkdf2_sha256(credentials.password)

    new_user = Users(None, credentials.username, password, **body)

    asyncio.create_task(db.insert_value(Tables.USERS.value, new_user))

    return json_response(new_user.response_format(), 201)


@user.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    user_info = await db.print_from_param(Tables.USERS.value, ("LOGIN", credentials.username))

    if user_info is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")

    temp_user = Users(*user_info)
    token, expiration_date = encryption.gen_access_token(str(temp_user.id))

    response = {
        "user": temp_user.response_format(),
        "token_info": {
            "token": token,
            "expiration_date": expiration_date
        }
    }

    return json_response(response)
