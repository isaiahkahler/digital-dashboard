import obd
# import os
# os.system("say hi")

connection = obd.OBD("/dev/ttyUSB0", baudrate=115200) 

# cmd = obd.commands.SPEED # select an OBD command (sensor)

# response = connection.query(cmd) # send the command, and parse the response

# print(response.value) # returns unit-bearing values thanks to Pint
# print(response.value.to("mph")) # user-friendly unit conversions

