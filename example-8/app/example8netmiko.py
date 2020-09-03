from netmiko import ConnectHandler

class Example8SSH:
    def __init__(self, ip, username, password, secret, device_type):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        self.device_type = device_type

        self.connection_details = {
            "ip": self.ip,
            "username": self.username,
            "password": self.password,
            "secret": self.secret,
            "device_type": self.device_type
        }

        self.ssh_session = None

    def connect(self):
        self.ssh_session = ConnectHandler(**self.connection_details)
        self.ssh_session.enable()

        return True

    def show_running_config(self, command="show run"):
        output  = self.ssh_session.send_command(command)
        return output