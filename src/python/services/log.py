from datetime import datetime as dt

from fastapi import Request


async def log_it(text: str, title: str, log_file_path='data/logs.txt'):
    with open(log_file_path, "a+") as f:
        f.write(f"[{dt.utcnow().strftime('%m/%d/%Y-%H:%M:%S')}] {title} \n{text}")


async def log_internal_server_error(request: Request):
    url = "http://" + request.url.hostname + request.url.path
    client = request.client.host + ":" + str(request.client.port)
    body = await request.json()
    headers = request.headers

    log_text = f"- URL: {url}\n- Client: {client}\n- Body: {body}\n- Headers: {headers}\n\n"

    await log_it(log_text, "INTERNAL SERVER ERROR LOG")
