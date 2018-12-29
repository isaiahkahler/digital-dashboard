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
    await websocket.recv()
    alerts = connection.query(obd.commands.GET_DTC).value
    await websocket.send(json.dumps({"alerts": alerts}))
    while True:
        data = {
            "speed": round(connection.query(obd.commands.SPEED).value.to('mph').magnitude ),
            "rpm": round(100 * (connection.query(obd.commands.RPM).value.magnitude / 8000)),
            "temp": min(100, round(
                    100 * (
                        (
                        max(195, connection.query(obd.commands.COOLANT_TEMP).value.magnitude) - 195
                        ) / 25
                    )
                )),
            "gas": round(connection.query(obd.commands.THROTTLE_POS).value.magnitude)
        }
        await websocket.send(json.dumps(data))
        time.sleep(0.1)


start_server = websockets.serve(socket_handler, 'localhost', 3001)


connection.watch(obd.commands.SPEED)
connection.watch(obd.commands.RPM)
connection.watch(obd.commands.COOLANT_TEMP)
connection.watch(obd.commands.THROTTLE_POS)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

os.system('serve -s build')
os.system('chromium-browser --kiosk http://localhost:3000')