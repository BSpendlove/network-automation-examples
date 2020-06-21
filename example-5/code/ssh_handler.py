from netmiko import Netmiko
import env_file

#This is a simple class that handles the SSH connection to a device and implements some very basic functions to create/list VLANs based on pure CLI scraping with Netmiko.
#Ensure that the env folder/file has been created as documented in app.py

class CiscoExample5:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.env_creds = env_file.get(path="env\ssh")

        self.ssh_details = {
            "device_type": "cisco_ios",
            "ip": self.ip,
            "port": self.port,
            "username": self.env_creds["SSH_USERNAME"],
            "password": self.env_creds["SSH_PASSWORD"],
            "secret": self.env_creds["SSH_SECRET"]
        }

        self.ssh_session = Netmiko(**self.ssh_details)
        self.ssh_session.enable()

    def create_vlan(self, vlan_id, vlan_name=""):
        if not self.validate_vlan(vlan_id):
            return {"error": True, "details": "Not a valid VLAN. Ensure this is passed as an integer to the function and is within the valid VLAN range"}

        if self.check_vlan_exist(vlan_id):
            return {"error": True, "details": "VLAN already exist on device"}

        cmds = ["vlan {}".format(vlan_id)]
        if vlan_name:
            cmds.append("name {}".format(vlan_name))

        self.ssh_session.send_config_set(cmds)

        #Perform verification check
        if self.check_vlan_exist(vlan_id):
           return {"error": False, "details": "VLAN {} has been successfully created".format(vlan_id)}
        else:
            return {"error": True, "details": "VLAN {} has not been successfully created".format(vlan_id)}

    def get_vlans(self):
        output = self.ssh_session.send_command("show vlan brief | begin 1")
        split_output = output.split("\n") #Assuming the above command pulls the right info, we can just split into lines, and then hard code the index splicing

        vlans = []
        for line in split_output:
            vlan = line.split()
            vlans.append({
                "vlan_id": int(vlan[0]), #0 will always be VLAN ID in Cisco IOS
                "vlan_name": vlan[1] #1 will always be VLAN Name in Cisco IOS
            })

        #Try to avoid when possible, hardcoding values like the above example...
        return vlans

    def check_vlan_exist(self, vlan_id):
        if not self.validate_vlan(vlan_id):
            return {"error": True, "details": "Not a valid VLAN. Ensure this is passed as an integer to the function and is within the valid VLAN range"}

        found_vlan = False
        vlans = self.get_vlans() # A function we implemented above to get the vlans in a python dictionary format to make it easier to loop through the vlans on the device

        for vlan in vlans:
            if vlan["vlan_id"] == vlan_id:
                found_vlan = True

        return found_vlan

    def validate_vlan(self, vlan_id): # Taken from example-2
        if isinstance(vlan_id, int):
            if vlan_id in range(1,4095):
                return True
        return False