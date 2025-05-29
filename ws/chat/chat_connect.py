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
        self.subscribed_rooms: set[str] = set()

    async def add_user_to_room(
        self, room_id: str, sender_id: str, websocket: WebSocket
    ) -> None:
        """
        Adds a WebSocket to a room using Redis for distributed tracking.
        """
        # await websocket.accept()
        sender_id = str(sender_id)
        self.local_sockets[sender_id] = websocket
        print("local_sockets", self.local_sockets)
        print("sender_id", sender_id)

        # Store in Redis
        await self.redis.sadd(f"room:{room_id}", sender_id)
        await self.redis.set(f"sender_id:{sender_id}", room_id)

        if room_id not in self.subscribed_rooms:
            await self.pubsub_client.connect()
            pubsub_subscriber = await self.pubsub_client.subscribe(room_id)
            asyncio.create_task(self._pubsub_data_reader(pubsub_subscriber, room_id))
            self.subscribed_rooms.add(room_id)

        # Attach socket_id to websocket object for cleanup
        websocket.sender_id = sender_id

    async def broadcast_to_room(self, room_id: str, message: str) -> None:
        """
        Publishes a message to Redis pubsub for a room.

        """
        print(f"[BROADCAST] room_id={room_id}, message={message}")
        await self.pubsub_client._publish(room_id, message)

    async def remove_user_from_room(self, room_id: str, websocket: WebSocket) -> None:
        """
        Removes a WebSocket from a room and cleans up Redis state.
        """
        sender_id = getattr(websocket, "sender_id", None)
        if sender_id:
            self.local_sockets.pop(sender_id, None)
            await self.redis.srem(f"room:{room_id}", sender_id)
            await self.redis.delete(f"sender_id:{sender_id}")

        members = await self.redis.smembers(f"room:{room_id}")
        if not members:
            await self.redis.delete(f"room:{room_id}")
            await self.pubsub_client.unsubscribe(room_id)
            self.subscribed_rooms.discard(room_id)

    async def _pubsub_data_reader(self, pubsub_subscriber, room_id: str):
        """
        Listens for Redis pubsub messages and sends them to all connected WebSockets.
        """
        print(f"[READER STARTED] for room: {room_id}")
        while True:
            try:
                message = await pubsub_subscriber.get_message(
                    ignore_subscribe_messages=True, timeout=1.0
                )
                if message:
                    raw_data = message["data"].decode("utf-8")
                    print(f"[RECEIVED] room={room_id}, data={raw_data}")

                    try:
                        data = json.loads(raw_data)
                    except json.JSONDecodeError:
                        print(f"[ERROR] Failed to decode JSON: {raw_data}")
                        continue

                    sender_ids = await self.redis.smembers(f"room:{room_id}")
                    print(f"[DELIVERING TO] {sender_ids}")

                    for sender_id in sender_ids:
                       
                        sender_id_str = sender_id.decode()
                        if sender_id_str == str(data.get("sender_id")):
                            continue
                        websocket = self.local_sockets.get(sender_id_str)
                        print("sender_id_str",sender_id_str)
                        print("websocket",websocket)

                        if websocket:
                            try:
                                await websocket.send_json(data)
                                print(f"[SENT] to sender_id={sender_id_str}")
                            except Exception as e:
                                print(f"[ERROR] Sending to {sender_id_str}: {e}")
                        else:
                            print(
                                f"[SKIP] sender_id={sender_id_str} not connected on this server"
                            )
            except Exception as e:
                print(f"[ERROR] Reader exception for room {room_id}: {e}")

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
