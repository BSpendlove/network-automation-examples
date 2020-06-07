# Handling credentials? We don't like hard coding credentials in our scripts so what's the best way to overcome this? It's extremely important if you want to share your code with other people!

from netmiko import ConnectHandler
import getpass # This is a very basic module that you can use to obtain a password without it displaying on the terminal console (python console/cmd/powershell/bash shell etc...)

username = input("Type your username: ") #input is also a module built into python for gathering input from the user... However you might not want to use input for 'automated' scripts...
password = getpass.getpass() #getpass.getpass? what's that all about... Well getpass is a module which also has a function called getpass... you could try: from getpass import get pass

ip = input("Type IP address: ")

netmiko_variables_dict = {
    "device_type": "cisco_ios", #Replace this device type if you'd like! You can see the supported device types on the official documentation
    "ip": ip,
    "username": username,
    "password": password,
    "secret": input("Enter secret: ") #Look here... We didn't store the secret as a variable? Technically, you shouldn't even of stored password as a variable because it's now stored in memory and can be found with a simple memory scanner or print(password)... You'll also see that the input() function with python will display your input on the terminal and therefore your secret is now exposed to that odd looking person over your right shoulder...
}

ssh_session = ConnectHandler(**netmiko_variables_dict)
output = ssh_session.send_command("show version")
print(output)

#Try typing an extremely weird sentence on the IP address input... Do you get an error? We're not handling any input from the user in this script so it'll break as soon as the IP address is wrong/invalid...