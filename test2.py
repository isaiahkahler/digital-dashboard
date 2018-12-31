import obd
import time

connection = obd.OBD()

while True:
    rpm = connection.query(obd.commands.RPM)
    speed = connection.query(obd.commands.SPEED)
    temp = connection.query(obd.commands.COOLANT_TEMP)
    print(rpm.value)
    print(speed.value)
    print(temp.value)