Example-5 shows how flask can be used to create a simple API to interact with a Cisco switch (creating/deleting vlans and showing information). It can be tweaked for other vendors but I try to include quite a few different examples such as:

- Python OOP
- Handling JSON Data in Flask (Body data)
- Using ENV files instead of hard coding usernames/passwords

The example will provide simple functions that work with Cisco IOS such as getting the VLANs:

```
HTTP GET
http://localhost:8080/192.168.0.252/get_vlans

RESPONSE:
{
"device": "192.168.0.252",
    "device_get_vlans": [
        {
            "vlan_id": 1,
            "vlan_name": "default"
        },
        {
            "vlan_id": 100,
            "vlan_name": "test"
        },
        {
            "vlan_id": 1002,
            "vlan_name": "fddi-default"
        },
        {
            "vlan_id": 1003,
            "vlan_name": "trcrf-default"
        },
        {
            "vlan_id": 1004,
            "vlan_name": "fddinet-default"
        },
        {
            "vlan_id": 1005,
            "vlan_name": "trbrf-default"
        }
    ]
}
```

Or creating a vlan and validating the input to ensure a VLAN doesn't exist:
```
HTTP POST

http://localhost:8080/192.168.0.252/create_vlan

BODY:
{
	"vlan_id": 224,
	"vlan_name": "test"
}

RESPONSE:
{
    "device": "192.168.0.252",
    "create_vlan": {
        "error": true,
        "details": "VLAN already exist on device"
    }
}
```