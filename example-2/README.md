example-2 demonstrates basic data validation checks to configure a VLAN on a cisco switch (Cisco IOS 15.x, Catalyst 3750G). In the first few examples, I try to only use Netmiko and native Python modules. CLI scraping can be a big pain in 2020 and it's recommended to either interact with the vendors API, use netconf or any other means that returns structured data because SSH scraping will require you to format the data in a usable format or you'll have a big headache working with the returned data. (not to mention your script will probably only work on a single platform/vendor)

The script demonstrates the following:

netmiko send_command/send_config_set
user input
data validation (VLAN is within the valid range)
basic error handling
implementing python functions
configuration verification after change