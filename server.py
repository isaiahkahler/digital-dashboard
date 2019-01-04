import obd
import asyncio
import websockets
import os
import time
import json

print('finished imports')

if len(obd.scan_serial()) == 0:
    connection = None
    print('connection to OBD-II could not be established')
else:
    # connection = obd.Async("/dev/ttyUSB0", baudrate=115200)
    connection = obd.OBD("/dev/ttyUSB0", baudrate=115200)
    print('connection to OBD-II was established')



async def producer_handler(websocket, path):
    if not not connection:
        alerts = connection.query(obd.commands.GET_DTC).value
        await websocket.send(json.dumps({ "alerts": alerts }))
        while True:
            rpm = connection.query(obd.commands.RPM)
            await asyncio.sleep(0.05)
            speed = connection.query(obd.commands.SPEED)
            await asyncio.sleep(0.05)

            if not rpm.is_null():
                await websocket.send(json.dumps({"rpm": 100 * (rpm.value.magnitude / 8000)}))

            if not speed.is_null():
                await websocket.send(json.dumps({"speed": round(speed.value.to('mph').magnitude)}))

async def consumer_handler(websocket, path):
    # async for message in websocket:
    while True:
        message = await websocket.recv()
        msg = json.loads(message)
        if 'show-camera' in msg and msg['show-camera'] == True:
            os.system('mplayer -slave -input file=/home/pi/digital-dashboard/fifofile tv:// -tv driver=v4l2:norm=NTSC_443:device=/dev/video0 -framedrop -fs &')
            await asyncio.sleep(45)
            os.system('echo "quit" > /home/pi/digital-dashboard/fifofile &')
        elif 'get-temp' in msg and msg['get-temp'] == True:
            time.sleep(0.05)
            temp = connection.query(obd.commands.COOLANT_TEMP)
            if not temp.is_null():
                temp = min(
                100,
                round(
                    100 * (
                        (max(60, temp.value.magnitude)) - 60) / 40 # measurement in celsius 
                    )
                )
                await websocket.send(json.dumps({"temp": temp}))
        # elif 'get-gas' in msg and msg['get-gas'] == True:
            # await asyncio.sleep(0.05)
            # gas = connection.query(obd.commands.FUEL_LEVEL)
            # if not gas.is_null():
            #     await websocket.send(json.dumps({"gas": gas .value.magnitude}))





async def socket_handler(websocket, path):
    # wait for client websocket
    await websocket.recv()
    print('connected to client')

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




start_server = websockets.serve(socket_handler, 'localhost', 3001)

print('websocket server started')

os.system('serve -s /home/pi/digital-dashboard/build &')
os.system('chromium-browser --kiosk --incognito http://localhost:5000 &')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()