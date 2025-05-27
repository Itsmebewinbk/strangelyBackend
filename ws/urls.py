from fastapi import APIRouter, WebSocket, WebSocketDisconnect,FastAPI
from datetime import datetime


router = APIRouter()
import logging

logger = logging.getLogger(__name__)


print(888888888888888888888888888)


# router.add_websocket_route("/ws/chat/{chat_id}", websocket_chat)



# @router.websocket("/chat/{chat_id}/")
# async def websocket_chat(websocket: WebSocket, chat_id: str):
#     await manager.connect(chat_id, websocket)
#     print(999999999999999999)
    
#     try:
#         while True:
#             user_id = 1  # Hardcoding user_id as 1
            
#             # Receive the message from the WebSocket
#             msg_text = await websocket.receive_text()
            
#             # Create the message document
#             message_doc = {
#                 "chat_id": chat_id,
#                 "user_id": user_id,
#                 "text": msg_text,
#                 "file": None,
#                 "created_at": datetime.utcnow()
#             }
            
#             # Get the async database connection
#             db = Depends(get_async_mongo)
#             await db["messages"].insert_one(message_doc)  # Save the message to the database

#             # Broadcast the message to all connected clients in the same chat
#             await manager.broadcast(chat_id, f"{user_id}: {msg_text}")

#     except WebSocketDisconnect:
#         # Handle WebSocket disconnection
#         manager.disconnect(chat_id, websocket)