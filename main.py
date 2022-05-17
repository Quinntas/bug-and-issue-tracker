import uvicorn
from fastapi import FastAPI

from src.python.routers.user import user

app = FastAPI()


@app.get("/")
async def home():
    return {"Hello": "World"}


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
