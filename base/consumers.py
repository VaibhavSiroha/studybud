from __future__ import annotations

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from typing import Any

from .models import Room, Message, User


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.group_name = f"room_{self.room_id}"

        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data: str | None = None, bytes_data: bytes | None = None) -> None:
        if not text_data:
            return
        data = json.loads(text_data)
        message_body = data.get("message")

        user: User | None = self.scope.get("user")
        if not message_body or not user or not user.is_authenticated:
            return

        room = await self.get_room(self.room_id)
        msg = await self.create_message(user_id=user.id, room_id=room.id, body=message_body)

        event = {
            "type": "chat.message",
            "message": msg.body,
            "username": user.username,
            "user_avatar_url": user.avatar.url if user.avatar else "",
            "message_id": msg.id,
            "created": msg.created.isoformat(),
        }

        # Broadcast to group
        await self.channel_layer.group_send(self.group_name, event)

    async def chat_message(self, event: dict[str, Any]) -> None:
        await self.send(text_data=json.dumps(event))

    # DB helpers
    @database_sync_to_async
    def get_room(self, room_id: str) -> Room:
        return Room.objects.get(id=room_id)

    @database_sync_to_async
    def create_message(self, user_id: int, room_id: int, body: str) -> Message:
        return Message.objects.create(user_id=user_id, room_id=room_id, body=body)


