from fastapi.responses import JSONResponse

from src.python.services.response import json_response


class ErrorCode(Exception):
    def __init__(self, code: int):
        self.code = code


def item_not_found() -> JSONResponse:
    return json_response({"error": "item not found"}, 404)


def unauthorized() -> JSONResponse:
    return json_response({"error": "unauthorized"}, 401)


def bad_request() -> JSONResponse:
    return json_response({"error": "bad request"}, 400)


def method_not_allowed() -> JSONResponse:
    return json_response({"error": "method not allowed"}, 405)


def internal_server_error() -> JSONResponse:
    return json_response({"error": "internal server error"}, 500)
