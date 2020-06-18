from flask import Flask, request
from ssh_handler import CiscoExample5
import json

app = Flask(__name__)

#Prior to running the flask app, ensure you have the requirements and that you create a folder called 'env' and then create file within that folder called 'ssh', a template can be found below:
# ./env/ssh
#
# SSH_USERNAME=myusername
# SSH_PASSWORD=mypassword
# SSH_SECRET=mysecret
#

@app.route("/test", methods=["GET"])
def test():
    return json.dumps({"test": True})

@app.route("/<string:device_ip>/check_vlan/<int:vlan_id>", methods=["GET"])
def device_check_vlan(device_ip, vlan_id):
    ssh_session = CiscoExample5(device_ip, 22)
    return json.dumps({
        "device": device_ip,
        "device_check_vlan": ssh_session.check_vlan_exist(vlan_id)
    }, indent=4)

@app.route("/<string:device_ip>/create_vlan", methods=["POST"])
def device_create_vlan(device_ip):
    #This function is created slightly differently, instead of passing the VLAN ID in the URL as a parameter, we're going to check the body data of the request.
    data = request.get_json()

    ssh_session = CiscoExample5(device_ip, 22)
    result = ssh_session.create_vlan(data["vlan_id"], data["vlan_name"])

    return json.dumps({
        "device": device_ip,
        "create_vlan": result
    }, indent=4)

@app.route("/<string:device_ip>/get_vlans", methods=["GET"])
def device_get_vlans(device_ip):
    ssh_session = CiscoExample5(device_ip, 22)
    return json.dumps({
        "device": device_ip,
        "device_get_vlans": ssh_session.get_vlans()
    }, indent=4)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)