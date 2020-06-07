from netmiko import ConnectHandler
import os
import re

class Device:
    def __init__(self, ip, username, password, secret, port=22, device_type="cisco_ios"): # Upon this class being initiated, we provide some key important steps to occur when creating the object...
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        self.port = port
        self.device_type = device_type

        self.netmiko_creds = {
            "ip": self.ip,
            "username": self.username,
            "password": self.password,
            "secret": self.secret,
            "port": self.port,
            "device_type": self.device_type
        }

        self.ssh_session = ConnectHandler(**self.netmiko_creds)
        self.ssh_session.enable()

    # Here is a very basic function to create a user, try to continue the code and validate basic user checks (such as length of username, special characters, etc..)
    # Try to also implement a validate function (eg. validate_cli_user) to check if the user has been successfully created before returning something back to the user
    def create_cli_user(self, username, password, priv_level=15, secret=True):
        command = None
        if secret:
            command = "username {} privilege {} secret {}".format(username, priv_level, password)
        else:
            command = "username {} privilege {} password {}".format(username, priv_level, password)
        
        return self.ssh_session.send_config_set(command)

    def get_hostname(self):
        self.ssh_session.set_base_prompt() # Upon changing hostname, base_prompt needs to refresh so we use set_base_prompt in case we've changed the hostname already
        prompt = self.ssh_session.base_prompt
        return prompt

    def set_hostname(self, hostname):
        if len(hostname) < 15:
            print("WARNING: Please avoid using hostnames longer than 15 characters")

        self.ssh_session.send_config_set(["hostname {}".format(hostname)])
        new_hostname = self.get_hostname()

        if new_hostname == hostname:
            return {"status": True, "details": "Hostname has been modified"}

        return {"status": False, "details": "Hostname has not been modified"}

    def get_interface(self, interface):
        output = self.ssh_session.send_command("show interfaces {} switchport".format(interface))
        split_output = output.split("\n")

        # Each line of our output is now in the list called split_output, here are many methods of abstracting some data, some bad, some good...
        interface_name = split_output[0].replace("Name: ", "") # Hard coding an index isn't the best thing to do, since it doesn't always guarantee valid data is returned
        switchport_status = split_output[1][12:] # String slicing which can produce varied results
        admin_mode = None
        access_vlan = None

        if switchport_status == "Enabled":
            for line in split_output:
                if "Administrative Mode:" in line:
                    admin_mode = line[21:] # String splicing again but not hardcoding the index, we try a substring match on Administrative Mode:

                if "Access Mode VLAN:" in line:
                    regex_match = re.findall(r'\d+', line) # Regex matching improves our slicing or hard coding strings, but can still produce wrong data if not used correctly
                    if regex_match:
                        access_vlan = regex_match[0]

        return {
            "interface": interface_name,
            "switchport_status": switchport_status,
            "admin_mode": admin_mode,
            "access_vlan": int(access_vlan) # Because our Validate VLAN check is against an integer, this will make it easier when we perform comparisons instead of converting the string to an integer at a later time...
        }

    def set_interface_vlan(self, interface, vlan_id):
        interface_config = self.get_interface(interface)

        # If switchport is disabled then it's probably a routed port
        # Also we need to check if the interface mode is access (static access or dynamic access), because this is not true if the port is routed or a trunk interface...
        if self.validate_vlan(vlan_id):
            if interface_config["access_vlan"] == vlan_id: # If the VLAN ID is already configured, let's return and not carry on with any code because it isn't necessary
                return {"status": False, "details": f"Interface access VLAN is already {vlan_id}"}

            if interface_config["switchport_status"] == "Enabled" and "access" in interface_config["admin_mode"]:
                commands = [f"interface {interface}", f"switchport access vlan {vlan_id}"]

                self.ssh_session.send_config_set(commands)

                new_interface_config = self.get_interface(interface) # Get the config again to see if the access VLAN has changed when we run 'show interfaces x switchport'.
                if new_interface_config["access_vlan"] == vlan_id:
                    return {"status": True, "details": "Interface access VLAN has been modified"}
        
        return {"status": False, "details": "Interface access VLAN has not been modified"}

    def validate_vlan(self, vlan_id):
        if isinstance(vlan_id, int):
            if vlan_id in range(1,4095): # This specifically means we can create VLANs between 1 and 4094 (0 and 4095 being reserved)... You can try to implement more checks for Cisco such as the reserved VLANs (1002-1005). Or to prompt the user about the VTP mode when configuring extended VLANs.
                return True
        return False