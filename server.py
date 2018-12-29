import obd
import asyncio
import websockets
import os
import time
import json

if len(obd.scan_serial()) == 0:
    connection = None
else:
    connection = obd.Async("/dev/ttyUSB0", baudrate=115200)



async def socket_handler(websocket, path):
    # wait for client websocket
    await websocket.recv()

    # send alerts or whatever
    alerts = connection.query(obd.commands.GET_DTC).value
    await websocket.send(json.dumps({ "alerts": alerts }))

    async def handle_speed(r):
        websocket.send(json.dumps({ "speed": round(r.value.magnitude ) }))

    async def handle_rpm(r):
        websocket.send(json.dumps({ "rpm": 100 * round(r.value.magnitude / 8000 ) }))
    
    async def handle_coolant(r):
        websocket.send(json.dumps({
            "temp": min(
                100,
                round(
                    100 * (
                        (max(195, r.value.magnitude) - 195) / 25
                    )
                )
            )
        }))
    
    async def handle_throttle(r):
        websocket.send(json.dumps({ "throttle": round(r.value.magnitude ) }))

    connection.watch(obd.commands.SPEED, callback=handle_speed)
    connection.watch(obd.commands.RPM, callback=handle_rpm)
    connection.watch(obd.commands.COOLANT_TEMP, callback=handle_coolant)
    connection.watch(obd.commands.THROTTLE_POS, callback=handle_throttle)
    connection.start()


start_server = websockets.serve(socket_handler, 'localhost', 3001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

os.system('serve -s build')
os.system('chromium-browser --kiosk http://localhost:3000')