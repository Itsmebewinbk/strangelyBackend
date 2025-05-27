from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict
from datetime import datetime
from db import get_async_mongo

#

async def save_message(data: Dict):
    try:
        db = await get_async_mongo()
        messages_collection = db["messages"]
        message_document = {
            "chat_id": data.get("chat_id"),
            "user_id": data.get("user_id"),
            "message": data.get("message"),
            "created_at": datetime.utcnow()
        }

        # Insert the message into the MongoDB collection
        await messages_collection.insert_one(message_document)
        print(f"Message saved: {data.get('message')}")
    except Exception as e:
        print(f"Error saving message: {e}")