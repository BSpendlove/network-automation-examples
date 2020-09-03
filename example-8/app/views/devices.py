from flask import Blueprint, render_template, request, flash, redirect, url_for
from forms import AddDevice
from functions import dbfunctions
from example8netmiko import Example8SSH
from functions import helpers

bp = Blueprint("devices", __name__, url_prefix="/devices")

@bp.route("", methods=["GET"])
def index():
    devices = dbfunctions.get_devices()
    return render_template("devices/index.html", devices=devices)

@bp.route("/add", methods=["GET", "POST"])
def add_device():
    form = AddDevice()
    form.authentication_user.choices = [user.username for user in dbfunctions.get_users()]
    if request.method == "POST":
        if form.validate_on_submit():
            device = dbfunctions.add_device(form.friendly_name.data, form.ip.data, form.netmiko_driver.data, form.authentication_user.data)
            if device:
                flash("Device {} was created.".format(device.friendly_name))
            return redirect(url_for("devices.index"))

    return render_template("devices/add_device.html", form=form)

@bp.route("/<int:id>/delete", methods=["DELETE"])
def delete_device(id):
    device = dbfunctions.delete_device(id)
    if not device:
        flash("Device {} was not found or deleted.".format(id))
    flash("Device {} was successfully deleted.")
    
    return redirect(url_for("devices.index"))

@bp.route("/<int:id>/view", methods=["GET", "POST"])
def view_device(id):
    device = dbfunctions.get_device(id)

    rootDir = "backups"
    dir_structure = helpers.dir_to_list(rootDir)

    vlan_holder = [{
        "id": 10,
        "name": "VLAN0010",
        "status": "Active"
    },
    {
        "id": 11,
        "name": "VLAN0011",
        "status": "Active"
    },
    {
        "id": 12,
        "name": "VLAN0012",
        "status": "Active"
    },
    {
        "id": 20,
        "name": "VLAN0020",
        "status": "Active"
    },
    {
        "id": 21,
        "name": "VLAN0021",
        "status": "Active"
    }]

    if request.method == "POST":
        config = None
        if "get_config" in request.form:
            ssh = Example8SSH(device.ip, device.user.username, device.user.password, device.user.password, device.netmiko_driver)
            ssh.connect()
            config = ssh.show_running_config()
        return render_template("devices/view_device.html", device=device, vlans=vlan_holder, running_config=config, folder_structure=dir_structure)
    if not device:
        flash("Error finding device {} in database".format(id))

    return render_template("devices/view_device.html", device=device, vlans=vlan_holder, running_config=config, folder_structure=dir_structure)