import asyncio
import websockets
import time
import json


async def socket_handler(websocket, path):
    await websocket.recv()

    async def handler():
        await websocket.send('hahaha')
        print('in the handler')

    while True:
        await handler()
        print ('called the handler')
        time.sleep(5)


start_server = websockets.serve(socket_handler, 'localhost', 3001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()