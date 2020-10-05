import env_file
import json
import time
import xmltodict
from ncclient import manager

device_details = env_file.get(path="env/ssh")

intf_brief = '''
<filter>
    <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-pfi-im-cmd-oper">
        <interface-briefs>
            <interface-brief>
            </interface-brief>
        </interface-briefs>
    </interfaces>
</filter>
'''

netconf_reply = None

with manager.connect(host=device_details["DEVICE"], port=830, username=device_details["USERNAME"],
    password=device_details["PASSWORD"], look_for_keys=False, device_params={'name':'iosxr'}) as m:

    output = m.get(intf_brief)
    netconf_reply = xmltodict.parse(str(output))

if not netconf_reply:
    raise ValueError('No NETCONF reply...')

time_start = time.time()

interfaces = []
interfaces_ = netconf_reply["rpc-reply"]["data"]["interfaces"]["interface-briefs"]["interface-brief"]

for interface in interfaces_:
    interface_ = {
        "interface": interface["interface"],
        "state": interface["state"],
        "line_state": interface["line-state"],
        "encapsulation": interface["encapsulation-type-string"],
        "mtu": int(interface["mtu"]),
        "bandwidth": int(interface["bandwidth"])
    }
    interfaces.append(interface_)

time_end = time.time()

time_took = time_end-time_start

print(json.dumps(interfaces, indent=4))
print("Time to execute script (excluding NETCONF functions):\n{}".format(time_took))
