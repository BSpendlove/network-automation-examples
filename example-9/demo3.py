import env_file
import json
import time
import textfsm
from netmiko import ConnectHandler

device_details = env_file.get(path="env/ssh")

device = ConnectHandler(**{
    "device_type": "cisco_xr",
    "ip": device_details["DEVICE"],
    "username": device_details["USERNAME"],
    "password": device_details["PASSWORD"]
})

command = "show interfaces brief"

output = device.send_command(command)
device.disconnect()

time_start = time.time()

interfaces = []

fsm_template = open("demo3.template")

fsm_handler = textfsm.TextFSM(fsm_template)

for obj in fsm_handler.ParseText(output):
    entry = {}
    for index, entry_value in enumerate(obj):
        entry[fsm_handler.header[index].lower()] = entry_value
    interfaces.append(entry)

time_end = time.time()

time_took = time_end-time_start

print(json.dumps(interfaces, indent=4))
print("Time to execute script (excluding Netmiko functions):\n{}".format(time_took))
