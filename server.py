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
    connection = obd.Async("/dev/ttyUSB0", baudrate=115200)
    print('connection to OBD-II was established')

is_established = False

async def socket_handler(websocket, path):
    # wait for client websocket
    await websocket.recv()
    async def handle_speed(r):
        value = r.value
        if not value:
            return

        await websocket.send(json.dumps({ "speed": round(value.magnitude ) }))

    async def handle_rpm(r):
        value = r.value
        if not value:
            return

        await websocket.send(json.dumps({ "rpm": 100 * round(value.magnitude / 8000 ) }))
    
    async def handle_coolant(r):
        value = r.value
        if not value:
            return

        await websocket.send(json.dumps({
            "temp": min(
                100,
                round(
                    100 * (
                        (max(195, value.magnitude) - 195) / 25
                    )
                )
            )
        }))
    
    async def handle_throttle(r):
        value = r.value
        if not value:
            return
        await websocket.send(json.dumps({ "throttle": round(value.magnitude ) }))


    if not connection:
        if is_established:
            connection.stop()
        # send alerts or whatever
        alerts = connection.query(obd.commands.GET_DTC).value
        await websocket.send(json.dumps({ "alerts": alerts }))
        connection.watch(obd.commands.SPEED, callback=await handle_speed)
        connection.watch(obd.commands.RPM, callback=await handle_rpm)
        connection.watch(obd.commands.COOLANT_TEMP, callback=await handle_coolant)
        connection.watch(obd.commands.THROTTLE_POS, callback=await handle_throttle)
        connection.start()
        is_established = True


start_server = websockets.serve(socket_handler, 'localhost', 3001)

print('websocket server started')

os.system('serve -s /home/pi/digital-dashboard/build &')
time.sleep(5)
os.system('chromium-browser --kiosk http://localhost:3000 &')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()