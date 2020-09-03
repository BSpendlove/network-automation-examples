class IOSVRouter():
    def __init__(
        self,
        hostname,
        interfaces=[]
        ):

            self.hostname = hostname
            self.interfaces = interfaces

    def set_hostname(self, hostname):
        self.hostname = hostname

    def add_interface(self, interface):
        self.interfaces.append(interface)

    def remove_interface(self, interface):
        del self.interfaces[interface]

    def __repr__(self):
        return "Example7.db_model.routers.IOSVRouter"

    def __str__(self):
        return str(self.__dict__)