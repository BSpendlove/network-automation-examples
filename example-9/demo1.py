import env_file
import json
import time
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

split_output = output.splitlines()

interface_start = [split_output.index(i) + 1 for i in split_output if "--------" in i]
if not interface_start:
    raise ValueError('Unable to find list index for interfaces...')

for interface in split_output[interface_start[0]:]:
    interface = interface.split()
    interface_ = {
        "interface": interface[0],
        "state": interface[1],
        "line_state": interface[2],
        "encapsulation": interface[3],
        "mtu": int(interface[4]),
        "bandwidth": int(interface[5])
    }
    interfaces.append(interface_)

time_end = time.time()

time_took = time_end-time_start

print(json.dumps(interfaces, indent=4))
print("Time to execute script (excluding Netmiko functions):\n{}".format(time_took))
