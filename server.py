import obd
import asyncio
import websockets
import os
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
            # throttle = connection.query(obd.commands.THROTTLE_POS)
            # asyncio.sleep(0.05)

            if not rpm.is_null():
                await websocket.send(json.dumps({"rpm": 100 * (rpm.value.magnitude / 8000)}))

            if not speed.is_null():
                await websocket.send(json.dumps({"speed": round(speed.value.to('mph').magnitude)}))

            # if not throttle.is_null():
            #     await websocket.send(json.dumps({"gas": throttle.value.magnitude}))

async def consumer_handler(websocket, path):
    # async for message in websocket:
    while True:
        message = await websocket.revc()
        msg = json.loads(message)
        if 'show-camera' in msg and msg['show-camera'] == True:
            print('fhsdjlfjdslkf djksl fjdslk fjds fjkds jfklds fkld sjfk djklf jdslkf jdskl fjsdk fjkdsl fjlds jfls')
            os.system('mplayer -slave -input file=/tmp/fifofile tv:// -tv driver=v4l2:norm=NTSC_443:device=/dev/video0 -framedrop -fs')
            asyncio.sleep(15)
            os.system('echo "quit" > /tmp/fifofile')
        elif 'get-temp' in msg and msg['get-temp'] == True:
            asyncio.sleep(0.05)
            temp = connection.query(obd.commands.COOLANT_TEMP)
            if not temp.is_null():
                temp = min(
                100,
                round(
                    100 * (
                        (max(90, temp.value.magnitude)) - 90) / 25 # measurement in celsius 
                    )
                )
                await websocket.send(json.dumps({"temp": temp}))



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
os.system('chromium-browser --start-fullscreen --disable-session-crashed-bubble --disable-infobars http://localhost:5000 &')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()