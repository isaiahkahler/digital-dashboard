import asyncio
import websockets
import time
import json


async def socket_handler(websocket, path):

    async def handler():
        await websocket.send('hahaha')
        print('in the handler')

    while True:
        await handler()
        print ('called the handler')
        time.sleep(5)

async def socket_handler2(websocket, path):
    def send_message(message):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(websocket.send(message))

    await websocket.recv()
    print('received')
    send_message('hi this is from python, and i kinda dont like it')

def socket_handler3(websocket, path):
    while True:
        websocket.send('hi this is from python, and i kinda dont like it')
        print('this is synchronous?')
        time.sleep(1)

start_server = websockets.serve(socket_handler3, 'localhost', 3001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

# async def myFunction():
#     print('hi')
