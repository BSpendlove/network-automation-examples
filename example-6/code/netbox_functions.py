import pynetbox
import env_file

def connect_nb():
    netbox_creds = env_file.get(path="env/netbox")
    nb = pynetbox.api(
        netbox_creds["NETBOX_URL"],
        token=netbox_creds["NETBOX_KEY"]
    )
    return nb

def get_devices():
    nb = connect_nb()

    return nb.dcim.devices.all()

def get_device_by_ip(ip):
    nb = connect_nb()
    devices = nb.ipam.ip_addresses.filter(ip)

    if not devices or len(devices) > 1:
        return None

    return devices[0].interface.device #This will return a Python Object which we can use

def get_vlan_by_site(vid, site, **kwargs):
    nb = connect_nb()
    return nb.ipam.vlans.get(vid=vid, site=site, **kwargs)

def get_vlan_group(slug):
    nb = connect_nb()
    return nb.ipam.vlan_groups.get(slug=slug) #Slug is a unique name so this should either return no results or 1 result

def create_vlan_group(site, name, slug):
    nb = connect_nb()
    return nb.ipam.vlan_groups.create(site=site, name=name, slug=slug)

def create_vlan(vid, name, status=1, **kwargs): #Required parameters are vid, name and status... By default status 1 = 'Active', 2 = 'Reserved', 3 = 'Deprecated'
    nb = connect_nb()
    return nb.ipam.vlans.create(vid=vid, name=name, status=status, **kwargs) #kwargs can be passed as optional variables