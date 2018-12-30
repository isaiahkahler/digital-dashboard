import asyncio
import websockets
import time
import json
import os
# from concurrent.futures import ProcessPoolExecutor
# from threading import Thread 

async def socket_handler(websocket, path):

    async def handler():
        await websocket.send('hahaha')
        print('in the handler')

    while True:
        await handler()
        print ('called the handler')
        time.sleep(5)

async def socket_handler2(websocket, path):
    async for message in websocket:
        print(message)
    

async def socket_handler3(websocket, path):
    async def send_message(message):
        await websocket.send("hello")

    print(await websocket.recv())
    # send_message('hello')
    loop = asyncio.get_event_loop()
    loop.create_task(send_message('hi'))


async def consumer_handler(websocket, path):
    print(websocket)
    while True:
        message = await websocket.recv()
        print(message)
    # async for message in websocket:
    #     print(message)
    #     await websocket.send(message + " response")
    print('listener terminated')

async def producer_handler(websocket, path):
    # print('hi')
    while True:
        message = "hello"
        await websocket.send(message)
        time.sleep(1)


async def socket_handler4(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


    # loop = asyncio.get_event_loop()
    # loop.create_task(send_messages())
    # loop.create_task(send_messages2())
    # loop.create_task(listener())


    # executor = ProcessPoolExecutor(2)
    # loop = asyncio.get_event_loop()
    # asyncio.ensure_future(loop.run_in_executor(executor, send_messages(websocket)))
    # asyncio.ensure_future(loop.run_in_executor(executor, send_messages2(websocket)))
        

start_server = websockets.serve(socket_handler4, 'localhost', 3001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
