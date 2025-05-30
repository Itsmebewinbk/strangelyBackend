# main.py
from fastapi import FastAPI, Request, HTTPException
from user.urls import router as urls_router
from chat.urls import router as chat_router
from ws.urls import router as ws_router
from sqladmin import Admin
from user.admin import UserAdmin, AdminAuth
from db import sync_engine, redis_client
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from response import ErrorResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, WebSocket,WebSocketDisconnect
from ws.chat import WebSocketManager,handle_websocket_messages
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()
from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# @app.middleware("http")
# async def catch_server_errors(request: Request, call_next):
#     response = await call_next(request)

#     if response.status_code >= 500:
#         log_data={
#             "request_method": request.method,
#             "user_id" : getattr(request.state, "user_id", None),
#             "url": request.url,
#             "status_code" : response.status_code
#         }
#         error_logger.error(log_data)

#         #sending the email...
#         subject = f"{os.getenv('APP_NAME')} - SERVER ERROR {log_data['status_code']}"
#         body = f"""
#         <html>
#           <body>
#             <h2>Server Error: 500</h2>
#             <p><strong>Method:</strong> {request.method}</p>
#             <p><strong>URL:</strong> {request.url}</p>
#             <p><strong>User ID:</strong> {getattr(request.state, 'user_id', None)}</p>
#             <p><strong>Status Code:</strong> {response.status_code}</p>
#             <hr>
#             <p style="font-size: 12px; color: gray;">Please check the server_errors.log.</p>
#           </body>
#         </html>
#         """
#         await send_error_email(subject, body)
#     return response





#exception_handling

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return ErrorResponse(
        message="The requested resource was not found", status_code=404
    )


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return ErrorResponse(message=exc.detail, status_code=exc.status_code)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return ErrorResponse(message="Internal server error", status_code=500)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    missing_fields = []
    for error in errors:
        if error["type"] == "missing":
            field_name = error["loc"][-1]
            missing_fields.append(f"{field_name} is required")

    message = missing_fields[0] if missing_fields else "Invalid request data"

    return ErrorResponse(message=message)



#sql_admin


admin = Admin(
    app,
    sync_engine,
    authentication_backend=AdminAuth(secret_key=SECRET_KEY),
    title="Strangely",
)
admin.add_view(UserAdmin)


@app.websocket("/ws/chats")
async def websocket_connect(websocket: WebSocket):
 
    await websocket.accept()
    await handle_websocket_messages(websocket)
    


# api/v1/
app.include_router(urls_router, prefix="/api/v1/users")
app.include_router(chat_router, prefix="/api/v1/chats")
