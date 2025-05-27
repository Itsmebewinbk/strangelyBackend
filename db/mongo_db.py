from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from fastapi import FastAPI


MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "chat_db"


sync_client = MongoClient(MONGO_URL)
sync_db = sync_client[DB_NAME]

async_client = AsyncIOMotorClient(MONGO_URL)
async_db = async_client[DB_NAME]

# Sync DB getter (sync client)
def get_sync_mongo():
    return sync_db

# Async DB getter (async client)
async def get_async_mongo():
    return async_db

# FastAPI app
app = FastAPI()

# # Startup event (for checking if MongoDB is available) 
# @app.on_event("startup")
# async def startup_db():
#     try:
#         # Test the connection (optional)
#         async_client.admin.command("ping")
#         print("MongoDB connected successfully.")
#     except Exception as e:
#         print(f"Error connecting to MongoDB: {e}")

# # Shutdown event (for closing the async client properly)
# @app.on_event("shutdown")
# async def shutdown_db():
#     print("Closing MongoDB client...")
#     async_client.close()  # Close the async client properly
