from netmiko import ConnectHandler # ConnectHandler will essentially handle the device vendor, obtain the correct class object and allow you to interact with the device based on the module support (eg. send_command being a generic function that is supported on all devices)

# ConnectHandler could also just be 'Netmiko' but official documentation prefers if you use ConnectHandler
# You can pass in variables into this object, mainly the few that are required are the device_type and using some common sense, ip/username/password

ssh_session = ConnectHandler(ip="192.168.0.252", device_type="cisco_ios", username="cisco", password="ciscodisco", secret="ciscodisco") # Here we pass in named variables and assign the ConnectHandler object to ssh_session so we can further interact with the class object
output = ssh_session.send_command("show version") # send_command is a very basic function that is used to send a command and return the output of the command... This is implemented on all device vendor classes however may be handled differently due to the vendors SSH implementation of the terminal. I assigned this function to 'output' because it actually returns data
print(output)

# You can pass in the named variables via a python dictionary and more specifically, using kwargs to allow us to pass the key to value mappings of a python dict. Have a look at the additional implementation below

netmiko_variables_dict = { # Don't ever let anybody bully you into renaming your variables because they are too long :-)
    "device_type": "cisco_ios",
    "ip": "192.168.0.252",
    "username": "cisco",
    "password": "ciscodisco",
    "secret" : "ciscodisco"
}

# Below is commented code, go ahead and copy this into a separate script with the above dictionary and uncomment out the code! You should not feel the need to always comment on every line of code, python is like plain english, it's quite obvious 99% of the time what the code is supposed to do...

# ssh_session = ConnectHandler(**netmiko_variables_dict)
# output = ssh_session.send_command("show version")
# print(output)