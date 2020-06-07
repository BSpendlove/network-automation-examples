from example3class import Device
from getpass import getpass

creds = {
    "ip": "192.168.0.252",
    "username": input("Enter Username: "),
    "password": getpass("Enter Password: "),
    "secret": getpass("Enter Secret: ")
}

# Here we initiate an object called myDevice
myDevice = Device(**creds)

# We now have the ability to use the functions/methods defined in the class 'Device'
myDevice.get_hostname()

print(myDevice.set_interface_vlan("G1/0/17", 106))

print(myDevice.create_cli_user("testuser", "testpassword"))