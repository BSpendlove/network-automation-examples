import env_file
import json
import time
import re
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

named_groups = ["interface", "state", "line_state", "encapsulation", "mtu", "bandwidth"]
interface_pattern = r"^\s+(?P<{}>\S+)\s+(?P<{}>up|down|admin-down)\s+(?P<{}>up|down|admin-down)\s+(?P<{}>\S+)\s+(?P<{}>\d+)\s+(?P<{}>\d+)$$".format(*named_groups)

for line in output.split("\n"):
    regex_match = re.search(interface_pattern, line)
    if not regex_match:
        continue

    interface_ = {}
    for name in named_groups:
        interface_[name] = regex_match.group(name)

    interfaces.append(interface_)

time_end = time.time()

time_took = time_end-time_start

print(json.dumps(interfaces, indent=4))
print("Time to execute script (excluding Netmiko functions):\n{}".format(time_took))
