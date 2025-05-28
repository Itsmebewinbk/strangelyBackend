import asyncio
import uuid
from fastapi import WebSocket
from redis.asyncio import Redis
from typing import Dict
from db.redis import RedisPubSubManager
import json
class WebSocketManager:
    def __init__(self):
        """
        Manages WebSocket connections across distributed servers using Redis.
        """
        self.local_sockets: Dict[str, WebSocket] = {}  # sender_id → WebSocket instance
        self.pubsub_client = RedisPubSubManager()
        self.redis = Redis()  # connect to your Redis host here

    async def add_user_to_room(self, room_id: str,sender_id:str, websocket: WebSocket) -> None:
        """
        Adds a WebSocket to a room using Redis for distributed tracking.
        """
        # await websocket.accept()
        sender_id = str(sender_id)
        self.local_sockets[sender_id] = websocket
        print("local_sockets",self.local_sockets)
        print("sender_id",sender_id)

        # Store in Redis
        await self.redis.sadd(f"room:{room_id}", sender_id)
        await self.redis.set(f"sender_id:{sender_id}", room_id)

        # Setup Redis pubsub if not already subscribed
        await self.pubsub_client.connect()
        pubsub_subscriber = await self.pubsub_client.subscribe(room_id)
        asyncio.create_task(self._pubsub_data_reader(pubsub_subscriber))

        # Attach socket_id to websocket object for cleanup
        websocket.sender_id = sender_id

    async def broadcast_to_room(self, room_id: str, message: str) -> None:
        """
        Publishes a message to Redis pubsub for a room.
        
        """
        print("room_id",room_id)
        await self.pubsub_client._publish(room_id, message)

    async def remove_user_from_room(self, room_id: str, websocket: WebSocket) -> None:
        """
        Removes a WebSocket from a room and cleans up Redis state.
        """
        socket_id = getattr(websocket, "socket_id", None)
        if socket_id:
            self.local_sockets.pop(socket_id, None)
            await self.redis.srem(f"room:{room_id}", socket_id)
            await self.redis.delete(f"socket:{socket_id}")

        # Optional: if no members left in Redis room set
        members = await self.redis.smembers(f"room:{room_id}")
        if not members:
            await self.redis.delete(f"room:{room_id}")
            await self.pubsub_client.unsubscribe(room_id)

    async def _pubsub_data_reader(self, pubsub_subscriber):
        """
        Reads messages from Redis PubSub and sends them to connected WebSockets.
        """
        while True:
            message = await pubsub_subscriber.get_message(ignore_subscribe_messages=True)
            if message is not None:
              
                room_id = message['channel'].decode('utf-8')
                
                data = message['data'].decode('utf-8')
                print("data_i_need",data)

                socket_ids = await self.redis.smembers(f"room:{room_id}")
                for socket_id in socket_ids:
                    socket = self.local_sockets.get(socket_id.decode())
                    if socket:
                        try:
                            data = json.loads(data)
                            await socket.send_json(data)
                        except Exception:


                            pass  # Optionally handle broken sockets here
    #     # STREAM VERSION of reading from the room
    # async def _stream_reader(self, room_id: str, websocket: WebSocket, consumer_id: str):
    #     group = f"group:room:{room_id}"
    #     stream = f"stream:room:{room_id}"

    #     # Create group if not exists
    #     try:
    #         await self.redis.xgroup_create(stream, group, id='0', mkstream=True)
    #     except Exception:
    #         pass  # Already exists

    #     while True:
    #         try:
    #             response = await self.redis.xreadgroup(
    #                 groupname=group,
    #                 consumername=consumer_id,
    #                 streams={stream: '>'},
    #                 count=1,
    #                 block=5000  # 5s timeout
    #             )
    #             if response:
    #                 for _, msgs in response:
    #                     for msg_id, msg_data in msgs:
    #                         await websocket.send_text(msg_data[b"msg"].decode())
    #                         await self.redis.xack(stream, group, msg_id)
    #         except Exception as e:
    #             print(f"Error reading from stream: {e}")
    #             break