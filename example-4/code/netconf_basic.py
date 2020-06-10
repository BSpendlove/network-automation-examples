from ncclient import manager
import env_file

credentials = env_file.get(path="env/netmiko")

m = manager.connect(
    host="192.0.2.1",
    username=credentials["SSH_USERNAME"],
    password=credentials["SSH_PASSWORD"],
    hostkey_verify=False,
    look_for_keys=False
)

for x in m.server_capabilities:
    print(x)

print(m.get_schema('ietf-interfaces'))
print(m.get_config(source='running'))