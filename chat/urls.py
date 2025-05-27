from fastapi import APIRouter, HTTPException

from chat.cruds import create_chat
from chat.schemas import Chat
router = APIRouter()
from typing import List, Optional
from fastapi import Depends
from db import get_async_mongo
@router.post("/chats/")
async def create_chat_route(chat_data: Chat, db=Depends(get_async_mongo)):
    try:
        return await create_chat(data=chat_data, db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))