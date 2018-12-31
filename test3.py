#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import time

async def hello():
    async with websockets.connect(
            'ws://localhost:3001') as websocket:
        await websocket.send("say heello jeebus")
        time.sleep(5)
        await websocket.send("say heello jeebus")
        time.sleep(5)
        await websocket.send("say heello jeebus")
        # greeting = await websocket.recv()
        # print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())