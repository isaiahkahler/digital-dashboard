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


async def socket_handler(websocket, path):  
    is_established = False

    # wait for client websocket
    await websocket.recv()
    print('connected to client')

    if not not connection:
        while True:
            rpm = connection.query(obd.commands.RPM).value
            if not not rpm:
                await websocket.send(json.dumps({"rpm": rpm.magnitude / 8000}))

            speed = connection.query(obd.commands.SPEED).value
            if not not speed:
                await websocket.send(json.dumps({"speed": speed.magnitude}))

            temp = connection.query(obd.commands.COOLANT_TEMP).value
            if not not temp:
                temp = min(
                100,
                round(
                    100 * (
                        (max(195, temp.magnitude)) - 195) / 25
                    )
                )
                await websocket.send(json.dumps({"temp": temp}))

            throttle = connection.query(obd.commands.THROTTLE_POS).value
            if not not throttle:
                await websocket.send(json.dumps({"gas": throttle.magnitude}))
            time.sleep(0.1)

    # define our handlers, will send data once OBD calls back
    # async def handle_speed(r):
    #     if not r:
    #         return
    #     await websocket.send(json.dumps({ "speed": round(r.value.magnitude ) }))

    # async def handle_rpm(r):
    #     if not r:
    #         return
    #     await websocket.send(json.dumps({ "rpm": 100 * round(r.value.magnitude / 8000 ) }))
    
    # async def handle_coolant(r):
    #     if not r:
    #         return
    #     await websocket.send(json.dumps({
    #         "temp": min(
    #             100,
    #             round(
    #                 100 * (
    #                     (max(195, value.magnitude) - 195) / 25
    #                 )
    #             )
    #         )
    #     }))
    
    # async def handle_throttle(r):
    #     value = r.value
    #     if not value:
    #         return
    #     await websocket.send(json.dumps({ "throttle": round(value.magnitude ) }))


    # if not connection:
    #     if is_established:
    #         connection.stop()
    #         connection.unwatch_all()
    #     # send alerts or whatever
    #     alerts = connection.query(obd.commands.GET_DTC).value
    #     await websocket.send(json.dumps({ "alerts": alerts }))
    #     connection.watch(obd.commands.SPEED, callback=handle_speed)
    #     connection.watch(obd.commands.RPM, callback=handle_rpm)
    #     connection.watch(obd.commands.COOLANT_TEMP, callback=handle_coolant)
    #     connection.watch(obd.commands.THROTTLE_POS, callback=handle_throttle)
    #     connection.start()
    #     is_established = True
    
    # async for message in websocket:
    #     msg = json.loads(message)
    #     if 'show-camera' in msg and msg['show-camera'] == True:
    #         os.system('mplayer -slave -input file=/home/pi/fifofile tv:// -tv driver=v4l2:norm=NTSC_443:device=/dev/video0 -framedrop -fs')
    #         time.sleep(10)
    #         os.system('echo "quit" > /home/pi/fifofile')




start_server = websockets.serve(socket_handler, 'localhost', 3001)

print('websocket server started')

os.system('serve -s /home/pi/digital-dashboard/build &')
time.sleep(5)
\
os.system('chromium-browser --kiosk http://localhost:5000 &')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()