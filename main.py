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
from ws.chat import WebSocketManager
from starlette.middleware.sessions import SessionMiddleware


import logging

logger = logging.getLogger(__name__)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

SECRET_KEY = "QDNWEJRNGERTIY3MRYT"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


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




admin = Admin(
    app,
    sync_engine,
    authentication_backend=AdminAuth(secret_key=SECRET_KEY),
    title="Strangely",
)
admin.add_view(UserAdmin)

# api/v1/
app.include_router(urls_router, prefix="/api/v1/users")
app.include_router(chat_router, prefix="/api/v1/chats")


@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}


ws_manager = WebSocketManager()

@app.websocket("/ws/chats")
async def websocket_connect(websocket: WebSocket):
    print(8222222222222222222222222222233333)
    await websocket.accept()
    room_id = None

    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")

            if command == "join_room":
                room_id = data.get("room_id")
                sender_id = data.get("sender_id")
                if room_id is None:
                    await websocket.send_json({"error": "room_id required"})
                    continue
                print(999999999999999999999999999999)
                await ws_manager.add_user_to_room(room_id,sender_id, websocket)

            elif command == "send_message":
                if room_id is None:
                    await websocket.send_json({"error": "You must join a room first"})
                    continue
                message = data.get("message")
                if message:
                    await ws_manager.broadcast_to_room(room_id, data)

            else:
                await websocket.send_json({"error": "Invalid command"})

    except WebSocketDisconnect:
        print(f"WebSocket disconnected from room {room_id}")
        await ws_manager.remove_user_from_room(room_id, websocket)