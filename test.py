import asyncio
import websockets
import time
import json


async def socket_handler(websocket, path):
    await websocket.recv()
    while True:
        print('lol')
        await websocket.send(json.dumps({"rmp": 30, "speed": "some number, probably"}))
        time.sleep(5)


start_server = websockets.serve(socket_handler, 'localhost', 3001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()