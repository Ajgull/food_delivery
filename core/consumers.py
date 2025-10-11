# import json

# from channels.generic.websocket import AsyncWebsocketConsumer


# class SupportConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add("support_group", self.channel_name)
#         await self.accept()
#         print(f"Client connected. Channel name: {self.channel_name}")

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("support_group", self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data["message"]
#         user = self.scope["client"]

#         await self.channel_layer.group_send(
#             "support_group",
#             {
#                 "type": "chat_message",
#                 "message": message,
#                 "sender_channel": self.channel_name,
#             },
#         )

#     async def chat_message(self, event):
#         sender_channel = event.get("sender_channel")
#         if sender_channel == self.channel_name:
#             return
#         message = event["message"]
#         await self.send(text_data=json.dumps({"message": message}))

import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class SupportConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        await self.channel_layer.group_add('support_group', self.channel_name)
        await self.accept()
        print(f'Client connected. Channel name: {self.channel_name}')

    async def disconnect(self, close_code: int) -> None:
        await self.channel_layer.group_discard('support_group', self.channel_name)
        print(f'Client disconnected. Channel name: {self.channel_name}')

    async def receive(self, text_data: str) -> None:
        data = json.loads(text_data)
        message = data['message']
        print(f'Message from client: {message}')

        await self.channel_layer.group_send(
            'support_group',
            {
                'type': 'chat_message',
                'message': message,
                'sender_channel': self.channel_name,
            },
        )

    async def chat_message(self, event) -> None:
        sender_channel = event.get('sender_channel')
        if sender_channel == self.channel_name:
            return
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        await self.accept()
        for i in range(5, 0, -1):
            await self.send(text_data=json.dumps({'countdown': i}))
            await asyncio.sleep(1)
        await self.send(text_data=json.dumps({'order_created': True}))
        await self.close()
