from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    devices = db.relationship("Device", backref="user", lazy='dynamic')

    def __repr__(self):
        return "<Example8 User {}>".format(self.id)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    friendly_name = db.Column(db.String)
    ip = db.Column(db.String)
    netmiko_driver = db.Column(db.String)
    authentication_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    vlans = db.relationship("VlanDump", backref="device", lazy=True)

    def __repr__(self):
        return "<Example8 Device {}>".format(self.id)

class VlanDump(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"))
    vlans = db.Column(db.Text)