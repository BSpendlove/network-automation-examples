Netmiko is an extremely handy tool that was written for Python to handle multiple vendors and to take care of the underlying SSH handling such as:

Reading from the SSH channel
Implementing OOP based vendor handling in a kind of 'modular' fashion so either the developer or others in the community can contribute unsupported vendors

Netmiko is essentially built ontop of Paramiko (which handles the underlying SSH protocol).

example-1 is aimed towards those not very familiar with Netmiko, providing different examples on how to connect to a device, how to connect to multiple devices, how to handle usernames/passwords, etc... in a pure python script environment.