Example-6 demonstrates interacting with an IPAM API (in our example it's Netbox, but the concept can be applied to any IPAM) so that we can sync the VLANs created on a Cisco switch and ensure that Netbox is always up to date with the latest information. We will achieve the following:

- Handle SSH to Cisco IOS device via Netmiko
- Grab VLANs and VLAN names similar to example-5
- Create a function for the initial device creation in Netbox to automatically fill out VLAN details (such as creating a VLAN Group for a site, and creating the VLANs)
- Perform some validation checks to prevent VLANs being recreated

If you would like to follow along this example or try it out yourself, I would recommend pulling the netbox docker container since it takes minutes to get up and running. Create an API key and use this in the script. Ensure there is a folder named 'env' and create 2 files called: 'ssh' and 'netbox' within this folder.

```
env/ssh
SSH_USERNAME=myusername
SSH_PASSWORD=mypassword
SSH_SECRET=mysecret
```

```
env/netbox
NETBOX_URL=http://url.or.ip.to.your.netbox:32768
NETBOX_KEY=0293YOUR0dj309API4902j3KEY
```