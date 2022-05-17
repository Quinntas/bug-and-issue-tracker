import uvicorn
from fastapi import FastAPI, Request

from src.python.exceptions import exceptions
from src.python.routers.user import user
from src.python.services.log import log_internal_server_error

app = FastAPI(
    title="Luna Bug Tracker",
    description="Personal luna bug tracker",
    version="1.0",
    contact={
        "name": "Caio Quintas",
        "email": "caioquintassantiago@gmail.com"
    },
    license_info={
        "name": "MIT"
    },
    terms_of_service="MIT"
)


@app.get("/")
async def home():
    return {}


@app.exception_handler(exceptions.ErrorCode)
async def error_code_exception(request: Request, exc: exceptions.ErrorCode):
    if exc.code == 404:
        return exceptions.item_not_found()

    if exc.code == 401:
        return exceptions.unauthorized()

    if exc.code == 400:
        return exceptions.bad_request()

    if exc.code == 405:
        return exceptions.method_not_allowed()

    if exc.code == 500:
        await log_internal_server_error(request)
        return exceptions.internal_server_error()

    await log_internal_server_error(request)
    return exceptions.internal_server_error()


# Routes
app.include_router(
    user,
    prefix="/user",
    tags=["user"]
)


def main():
    host = '192.168.100.58'
    port = 5000

    uvicorn.run("main:app", host=host, port=port, server_header=False)


if __name__ == "__main__":
    main()
