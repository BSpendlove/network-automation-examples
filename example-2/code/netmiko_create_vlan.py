from getpass import getpass
from my_devices import devices_cisco_ios
from netmiko import ConnectHandler

def create_vlan(ssh_session, vlan_id, vlan_name):
    try:
        ssh_session.enable()

        if validate_vlan(vlan_id):
            if verify_vlan(ssh_session, vlan_id): # If VLAN already exist, return and do nothing...
                return
            commands = [f"vlan {vlan_id}", f"name {vlan_name}", "exit"]
            # or you can do something like -> commands = ["vlan {}".format(vlan_id), "name {}".format(vlan_name)]

            output = ssh_session.send_config_set(commands)
            return output
    except Exception as error:
        print(error)

def validate_vlan(vlan_id):
    if isinstance(vlan_id, int):
        if vlan_id in range(1,4095): # This specifically means we can create VLANs between 1 and 4094 (0 and 4095 being reserved)... You can try to implement more checks for Cisco such as the reserved VLANs (1002-1005). Or to prompt the user about the VTP mode when configuring extended VLANs.
            return True
    return False

def verify_vlan(ssh_session, vlan_id):
    output = ssh_session.send_command(f"show vlan id {vlan_id}")

    if f"{vlan_id} not found in current VLAN database" in output: # Very simple string match that works on Cisco IOS platform
        print("VLAN does not exist...\n")
        return False
    else:
        print("VLAN exists...\n")
        return True

def remove_vlan(ssh_session, vlan_id):
    try:
        ssh_session.enable()

        if validate_vlan(vlan_id):
            commands = [f"no vlan {vlan_id}"]

            output = ssh_session.send_config_set(commands)
            return output
    except Exception as error:
        print(error)

for device in devices_cisco_ios:
    netmiko_dictionary = {
        "device_type": device["device_type"],
        "ip": device["ip"],
        "username": device["username"],
        "password": device["password"],
        "secret": device["secret"]
    }

    ssh_session = ConnectHandler(**netmiko_dictionary)

    vlan_id = int(input("Enter VLAN ID: ")) # Here we convert the user input to an integer. This will be used in the validate_vlan function to check if the variable is an integer
    vlan_name = input("Enter VLAN Name: ")

    created_vlan = create_vlan(ssh_session, vlan_id, vlan_name)

    if created_vlan:
        verified_vlan = verify_vlan(ssh_session, vlan_id)

    ask_to_remove = input("Remove VLAN? [y/n]: ")

    if ask_to_remove.lower() == "y":
        remove_vlan(ssh_session, vlan_id)
        verified_vlan = verify_vlan(ssh_session, vlan_id)

# The whole purpose of this extremely basic script (which still has errors, try to find them!) is to demonstrate the purpose of using functions to consolidate basic actions that we perform as a network engineer, such as checking if the VLAN exist, if it doesn't then why would we try to delete a non-existent VLAN?... A lot of basic error handling/checking I find personally is related to common sense and knowing the platform (and how it would react if eg. you added a VLAN to a switch running as a VTP client, or adding a VLAN out of the valid VLAN range)

# Please remember this script is not a perfect demonstration on creating a VLAN but trying to demonstrate a basic logic of functions and give a general overview to the reader on what things they will need to perform basic validation checks and code optimization.