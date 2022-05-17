from fastapi import Request, HTTPException

from src.python.services import encryption


def token_required(handler):
    async def wrapper(request: Request, *args, **kwargs):
        if 'x-access-token' not in request.headers.keys():
            raise HTTPException(status_code=400, detail="BAD REQUEST")

        if encryption.verify_access_token(request.headers['x-access-token']) is False:
            raise HTTPException(status_code=401, detail="UNAUTHORIZED")

        return await handler(*args, **kwargs)

    # Fix signature of wrapper
    import inspect
    wrapper.__signature__ = inspect.Signature(
        parameters=[
            # Use all parameters from handler
            *inspect.signature(handler).parameters.values(),

            # Skip *args and **kwargs from wrapper parameters:
            *filter(
                lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
                inspect.signature(wrapper).parameters.values()
            )
        ],
        return_annotation=inspect.signature(handler).return_annotation,
    )

    return wrapper
