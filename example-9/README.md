Example-9 demonstrates 4 different ways to obtain interfaces on a Cisco IOS-XR device.

1) List Indexing and String Splicing - Pure Python
2) re module
3) textfsm module
4) netconf XML filter

You can find the examples as a format demox.py where x is the type of approach above...

If you want to try these examples yourself, you will need to install the requirements (pip install -r requirements.txt) and also copy the example-env folder, rename it to "env" and input an XR device capable of NETCONF, your username and password.