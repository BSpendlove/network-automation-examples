import env_file
import sys
import netbox_functions
from netmiko import Netmiko

def ssh_session(ip):
    #This establishes the SSH session using Netmiko
    ssh_creds = env_file.get(path="env/ssh")
    netmiko_creds = {
        "device_type": "cisco_ios",
        "ip": ip,
        "username": ssh_creds["SSH_USERNAME"],
        "password": ssh_creds["SSH_PASSWORD"],
        "secret": ssh_creds["SSH_SECRET"]
    }

    netmiko_session = Netmiko(**netmiko_creds)
    netmiko_session.enable()
    return netmiko_session

def get_vlans(ssh_session, exclude_vlans=[1, 1002, 1003, 1004, 1005]):
    cli_output = ssh_session.send_command("show vlan brief | begin 1")

    split_output = cli_output.split("\n") #Assuming the above command pulls the right info, we can just split into lines, and then hard code the index splicing

    vlans = []
    for line in split_output:
        vlan = line.split()

        if int(vlan[0]) in exclude_vlans: #By default we don't want to record the default VLANs on a cisco switch
            continue

        vlans.append({
            "id": int(vlan[0]), #0 will always be VLAN ID in Cisco IOS, we'll ensure this is returned as an integer because it's easier to work with when performing other tasks...
            "name": vlan[1] #1 will always be VLAN Name in Cisco IOS
        })

    #Try to avoid when possible, hardcoding values like the above example...
    return vlans

def create_netbox_info(ssh_session, update_vlans=True): #if update_vlans is set to False, then VLANs that don't match Netbox will not be updated (eg. VLAN name changed)
    device = netbox_functions.get_device_by_ip(ssh_session.host) #If the primary IP address used to SSH isn't recorded in Netbox then not much will happen
    if device:
        vlan_group_slug = "{}-l2-group".format(device.site.slug) # We'll set the name here in a variable because we will use this a few times in our script instead of formatting strings everytime...
        check_vlan_group = netbox_functions.get_vlan_group(vlan_group_slug)
        netbox_vlan_group = None

        if check_vlan_group:
            # We have found a VLAN Group according to our format above 'sitename-l2-group'
            netbox_vlan_group = check_vlan_group
        else:
            # No VLAN Group exist so we need to create one
            netbox_vlan_group = netbox_functions.create_vlan_group(device.site.id, "{} Layer 2 Group".format(device.site.name), "{}".format(vlan_group_slug))

        vlans = get_vlans(ssh_session) #Netmiko time, get_vlans should in most cases return a dictionary of VLANs assuming this is a Cisco switch running IOS 15.x+
        for vlan in vlans:
            check_vlan = netbox_functions.get_vlan_by_site(vlan["id"], device.site.slug, group=netbox_vlan_group.slug) #To avoid trying to create the VLAN again, we will simply print a statement if it already exist. Maybe you can write a different function for the ability of modifying existing VLANs (which we will need to do for the sync script...)
            if check_vlan:
                if update_vlans: # If True, we can reference variables as vlan.x where x is changable such as name, description, tags, etc...
                    print("VLAN {} found...\nOld Name: {}\nNew Name: {}\n".format(check_vlan.vid, check_vlan.name, vlan["name"]))
                    check_vlan.name = vlan["name"]
                    check_vlan.save()
                else:
                    print("VLAN {} ({}) already exist in VLAN group '{}'...".format(check_vlan.vid, check_vlan.name, netbox_vlan_group.name))
            else:
                #VLAN doesn't exist on site/vlan group...
                print("Creating new VLAN {} for VLAN Group '{}'...".format(netbox_functions.create_vlan(vlan["id"], vlan["name"], site=device.site.id, group=netbox_vlan_group.id).vid, netbox_vlan_group.name))
    else:
        print("Could not find device with IP address: {}...".format(ssh_session.host))

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("IP address needs to be passed as an argument...")
        sys.exit()

    ip_address = sys.argv[1]
    ssh_session = ssh_session(ip_address)
    create_netbox_info(ssh_session)

    #We should amend this script so that the basic netbox check is performed prior to SSH because SSH can take some time whereas a quick query to the netbox API can reduce the time it takes to encounter an issue such as the device not already created in netbox.