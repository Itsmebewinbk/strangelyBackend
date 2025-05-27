import logging
from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR
from response import ErrorResponse

error_logger = logging.getLogger("error_logger")
request_logger = logging.getLogger("request_logger")

async def custom_exception_handler(request: Request, exc: Exception):
    try:
        request_data = {
            "data": await request.json() if request.method in ["POST", "PUT", "PATCH"] else None,
            "query": dict(request.query_params)
        }
    except Exception:
        request_data = {"query": dict(request.query_params)}

    request_logger.info(f"Request Data: {request_data}")
    error_logger.error(f"Exception: {str(exc)}", exc_info=True)

    if isinstance(exc, HTTPException):
        if exc.status_code == HTTP_401_UNAUTHORIZED:
            return ErrorResponse(status_code=HTTP_401_UNAUTHORIZED, message="Unauthorized: Access is denied.")
        elif exc.status_code == HTTP_403_FORBIDDEN:
            return ErrorResponse(status_code=HTTP_403_FORBIDDEN, message=str(exc.detail))
        else:
            return ErrorResponse(status_code=exc.status_code, message=str(exc.detail))

    return ErrorResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        message="Server is facing technical difficulties, please try again later."
    )
