from db_models.interface import Interface
from db_models.routers import IOSVRouter
import json

interfaces = [
    {
        "name": "GigabitEthernet0/0/0/0",
        "speed": 1000,
        "duplex": "full",
        "encapsulation": ""
    },
    {
        "name": "GigabitEthernet0/0/0/1",
        "speed": 1000,
        "duplex": "full",
        "encapsulation": ""
    },
    {
        "name": "GigabitEthernet0/0/0/2",
        "speed": 1000,
        "duplex": "full",
        "encapsulation": ""
    },
    {
        "name": "GigabitEthernet0/0/0/3",
        "speed": 1000,
        "duplex": "full",
        "encapsulation": ""
    },
    {
        "name": "GigabitEthernet0/0/0/4",
        "speed": 1000,
        "duplex": "full",
        "encapsulation": ""
    }
]

router = IOSVRouter("vios1")

for interface in interfaces:
    _interface = Interface()

    _interface.name = interface["name"]
    _interface.speed = interface["speed"]
    _interface.duplex = interface["duplex"]
    _interface.encapsulation = interface["encapsulation"]
    router.add_interface(_interface)

print(router)