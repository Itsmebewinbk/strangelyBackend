from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional


class ErrorResponse(JSONResponse):
    def __init__(self, message: str, status_code: int = 400):
        content = {
            "status_code": status_code,
            "message": message,
            "status": "error",
        }
        super().__init__(content=content, status_code=status_code)


class SuccessResponse(JSONResponse):
    def __init__(
        self, message: str, data: Optional[dict] = None, status_code: int = 200
    ):
        content = {
            "status": "ok",
            "status_code": status_code,
            "message": message,
            "data": data,
        }
        super().__init__(content=content, status_code=status_code)
