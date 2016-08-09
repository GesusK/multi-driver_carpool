__author__ = 'Arthur'
"""
This class is used as a data structure for passenger/driver.
"""
class Member():

    name = None
    address = None
    coord = None
    isDriver = None
    psg_list = None

    def __init__(self, name, addr, isDriver=False):
        if (not name or not addr ):
            print("Error: Member input must has name, address")
            return None;
        self.name = name
        self.address = addr
        self.isDriver = isDriver
        if self.isDriver:
            self.psg_list = list()

    # getters
    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_coord(self):
        if self.coord:
            return self.coord
        else:
            print("Error: Coord not set yet")
            return None

    def isDriver(self):
        return self.isDriver

    # setter for coord
    def set_coord(self, coord):
        self.coord = coord

    def add_psg(self, member):
        self.psg_list.append(member)

    def show_member(self):
        print("Member: " + self.name +
              "; Address: " + self.address +
              "- " + self.coord.get("lat") +
              ", " + self.coord.get("lng"))


if __name__ == '__main__':
    arthur = Member("Arthur", "GTA")
    arthur.show_member()