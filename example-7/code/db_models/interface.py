class Interface():
    def __init__(self):
        self.name = "",
        self.speed = 0,
        self.duplex = ""
        self.encapsulation = ""

    def set_name(self, name):
        self.name = name

    def set_speed(self, speed):
        if(isinstance(speed, int)):
            self.speed = speed
        else:
            raise ValueError("Speed is not an integer")

    def set_duplex(self, duplex):
        valid_duplex = ["full", "half"]
        if duplex.lower() in valid_duplex:
            self.duplex = duplex
        else:
            raise ValueError("Invalid duplex type. Valid duplexs are {}".format(valid_duplex))

    def set_encapsulation(self, encapsulation):
        valid_encapsulation = ["Ethernet", "PPP", "HDLC"]
        if encapsulation.lower() in valid_encapsulation:
            self.encapsulation = encapsulation
        else:
            raise ValueError("Invalid encapsulation type. Valid encapsulations are {}".format(valid_encapsulation))

    def __repr__(self):
        return "Example7.db_models.interface.Interface"

    def __str__(self):
        return str(self.__dict__)

    def __setattr__(self, name, value):
        self.__dict__[name] = value