from code.supports import Importer as I


class Instance(object):

    def __init__(self, my_space, my_vehicle, my_number=0):
        self.space = my_space
        self.vehicle = my_vehicle
        self.number_of_vehicles = my_number  # TODO: default min number from space info

    def set_number_of_vehicles(self, my_number):
        self.number_of_vehicles = my_number

    def get_space(self):
        return self.space

    def get_node_coordinates(self):
        pass

    def get_adjacency_matrix(self):
        pass

    def get_delivery_array(self):
        pass

    def get_problem_info(self):
        pass

    def get_vehicle(self):
        pass
class Space(object):
    pass


class Vehicles(object):
    pass
