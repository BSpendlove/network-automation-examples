# What if we want to run a send_command on 100 different devices and store the output in a file...? We could just create 100 different scripts or copy+paste our blocks of code 100 times and change the IP address but here are a few ways...
from netmiko import ConnectHandler

# Hard coding IP addresses in a python list
# We can store multiple IP addresses in a list and use some basic python logic such as a 'for' loop to access each index of the list (eg.. item1, item2, item3, item4)

ip_addresses = ["192.168.0.252", "192.168.0.253", "192.168.0.254"]

for ip in ip_addresses:
    print(ip)

    netmiko_variables_dict = {
    "device_type": "cisco_ios",
    "ip": ip, # Here we can reference the item that is currently stored as  variable 'ip' in the list. When we are finished with the first IP address 192.168.0.252, the same code that is contained within this for loop will proceed to run on the next item in our list...
    "username": "cisco",
    "password": "ciscodisco",
    "secret" : "ciscodisco"
    }

    #ssh_session = ConnectHandler(**netmiko_variables_dict)
    #output = ssh_session.send_command("show version")
    #print(output)

# What if I had different device vendor types with different usernames, passwords and secrets?
# You can get really complicated to the point where you can pull data about IP addresses from some kind of IPAM database, or your credentials from a password vault by interacting with it's API. Here is a few easy methods to get those starting with Python as an introduction to different data types etc...

# This is a dictionary that contains each device with related information to that device
#====================================================================#
# Example 1

devices = {
    "switch01": {
        "device_type": "cisco_ios",
        "ip": "192.168.0.252",
        "username": "cisco",
        "password": "ciscodisco",
        "secret": "ciscodisco"
    },
    "switch02": {
        "device_type": "cisco_nxos",
        "ip": "192.168.0.253",
        "username": "admin",
        "password": "nopassword",
        "secret": "ultrasecret..secret"
    },
    "firewall21": {
        "device_type": "paloalto_panos",
        "ip": "192.168.0.254",
        "username": "panman",
        "password": "dingdong",
        "secret": "wooopdescoopde"
    }
}

for device in devices:
    netmiko_variables_dict = {
    "device_type": devices[device]["device_type"],
    "ip": devices[device]["ip"],
    "username": devices[device]["username"],
    "password": devices[device]["password"],
    "secret" : devices[device]["secret"]
    }

    print(netmiko_variables_dict)
#====================================================================#

#====================================================================#
# Example 2
devices = [{
        "device_type": "cisco_ios",
        "ip": "192.168.0.252",
        "username": "cisco",
        "password": "ciscodisco",
        "secret": "ciscodisco"
    },
    {
        "device_type": "cisco_nxos",
        "ip": "192.168.0.253",
        "username": "admin",
        "password": "nopassword",
        "secret": "ultrasecret..secret"
    },
    {
        "device_type": "paloalto_panos",
        "ip": "192.168.0.254",
        "username": "panman",
        "password": "dingdong",
        "secret": "wooopdescoopde"
    }]

for device in devices:
    netmiko_variables_dict = {
    "device_type": device["device_type"],
    "ip": device["ip"],
    "username": device["username"],
    "password": device["password"],
    "secret" : device["secret"]
    }

    print(netmiko_variables_dict)
#====================================================================#

#====================================================================#
# Example 3
ip_addresses = ["192.168.0.252", "192.168.0.253", "192.168.0.254"]
netmiko_variables_dict = {
    "device_type": "cisco_ios",
    "ip": None,
    "username": "cisco",
    "password": "ciscodisco",
    "secret" : "ciscodisco"
    }

for ip in ip_addresses:
    netmiko_variables_dict.update({"ip": ip}) # Here we update the key 'ip' with the value of the variable 'ip'... Each time this for loop iterates through the list of IP addresses, the dictionary device_type, username and password stays the same but the IP address changes...
    print(netmiko_variables_dict["ip"])
#====================================================================#

#====================================================================#
# Example 4
import examplepassword # Try to avoid adding import statements half way in a script (or anywhere except from the top)...

print(examplepassword.my_username)
print(examplepassword.my_password)
print(examplepassword.my_secret)
#====================================================================#

#====================================================================#
# Example 5 (Reading IP addresses from txt file)

# Create a txt file called ip_addresses.txt and add an IP address to each line
with open("ip_addresses.txt", "r") as txt_ip_addresses: # Be careful with statements like this... Depending on how you run the script or the operating system, you may get various results. Run the script via shell in the directory where the txt file exist to avoid any errors regarding IO file exist etc...
    for ip_address in txt_ip_addresses.readlines():
        print(ip_address)
#====================================================================#

# By all means, these methods of storing IP addresses, usernames, passwords and secrets are not to demonstrate how you SHOULD do it, but what you can do.
# As mention previously, you can interact with APIs, Password Vaults, encryption modules, only user input, environment variables, databases but it is up to you to decide what you will use.