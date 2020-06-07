example-3 demonstrates basic OOP logic to configure spanning-tree protocol on a Cisco IOS (Catalyst) switch. We are still trying to use as much native python as we can (with the exception of Netmiko to handle our SSH session to the device). One of the module requirements for Netmiko that will be installed automatically is textfsm. This is an alternative solution when the only option we have is CLI scraping because it allows us to match import data using regex patterns and store the data in a much more efficent format for accessing in our python script. However in this example, we will be using raw python to try to filter out data to give the reader an idea how complicated it can get compared to using something like Textfsm or Netconf.

-Change hostname of device
-Create a basic local user
-Change the access vlan of an interface
-Return interface data (access vlan, interface mode)