
from datetime import datetime
import uuid


async def create_chat(data, db):
   
    chat_type = data.chat_type
    name = data.name
    image = data.image
   
   
    chat_id = uuid.uuid4()

    members_data = [
        {"chat_id": str(chat_id), "user_id": member.user_id}
        for member in data.members
    ]
    chat_data = {
        "id": str(chat_id), 
        "chat_type": chat_type,
        "members":members_data,
        "name": name,
        "image": image,
       
       
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    await db["chats"].insert_one(chat_data)
    data ={
        "chat_id":str({chat_id})
    }

    return {
        
        "data": data,
        "message": "Chat created successfully"
    }
    