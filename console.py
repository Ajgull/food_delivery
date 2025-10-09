# import os

# import django
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
# django.setup()

# channel_layer = get_channel_layer()


# def send_message(channel_name, message):
#     async_to_sync(channel_layer.send)(
#         channel_name,
#         {
#             "type": "chat_message",
#             "message": message,
#         },
#     )


# if __name__ == "__main__":
#     channel_name = input("Введите channel_name клиента (выводится в консоли): ")
#     while True:
#         msg = input("Введите сообщение для клиента (или exit для выхода): ")
#         if msg.lower() == "exit":
#             break
#         send_message(channel_name, msg)


import asyncio
import json
import os

import django
import websockets

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

WS_URL = 'ws://localhost:8000/ws/support/'


async def listen_and_send() -> None:
    async with websockets.connect(WS_URL) as websocket:
        print('Подключено к серверу поддержки')

        async def send_messages() -> None:
            while True:
                msg = await asyncio.get_event_loop().run_in_executor(
                    None, input, 'Введите сообщение для клиента (или exit): '
                )
                if msg.lower() == 'exit':
                    break
                await websocket.send(json.dumps({'message': msg}))

        async def receive_messages() -> None:
            async for message in websocket:
                data = json.loads(message)
                print(f'Сообщение от клиента: {data.get("message")}')

        send_task = asyncio.create_task(send_messages())
        receive_task = asyncio.create_task(receive_messages())
        done, pending = await asyncio.wait(
            [send_task, receive_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()


if __name__ == '__main__':
    asyncio.run(listen_and_send())
