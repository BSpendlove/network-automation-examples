from app import db
from models import User, Device

def add_user(username, password):
    user = User(
        username=username,
        password=password
    )
    db.session.add(user)
    db.session.commit()
    return user

def delete_user(id):
    user = get_user(id)
    if not user:
        return False
    
    db.session.delete(user)
    return True

def get_user(id):
    user = None
    if isinstance(id, str):
        user = User.query.filter_by(username=id).first()
    else:
        user = User.query.get(id)
    if not user:
        return False
    return user

def get_users():
    return User.query.all()

def add_device(friendly_name, ip, netmiko_driver, authentication_user):
    authentication_user = get_user(authentication_user)
    device = Device(
        friendly_name=friendly_name,
        ip=ip,
        netmiko_driver=netmiko_driver,
        authentication_user=authentication_user.id if authentication_user else None
    )
    db.session.add(device)
    db.session.commit()
    return device

def delete_device(id):
    device = get_device(id)
    if not device:
        return False

    db.session.delete(device)
    return True

def get_device(id):
    device = None
    if isinstance(id, str):
        device = Device.query.filter_by(friendly_name=id).first()
    else:
        device = Device.query.get(id)
    if not device:
        return False
    return device

def get_devices():
    return Device.query.all()