from fastapi.responses import JSONResponse


def json_response(content: dict, status_code: int = 200):
    headers = {
        "server": "Quintas's Servers",
        "content-language": "en-US",
        "content-type": 'application/json',
        "cache-control": 'no-cache, no-store'
    }
    return JSONResponse(content=content, headers=headers, status_code=status_code)
