# TODO: add checking if route/node is fisible!


class ProblemInstance(object):

    def __init__(self, my_info, my_network, my_fleet, my_distance_matrix):
        self.name = my_info['NAME']
        self.description = my_info['COMMENT']
        self.type = my_info['TYPE']
        self.network = my_network
        self.fleet = my_fleet  # TODO: default min number from space info
        self.distance_matrix = my_distance_matrix
        self.drawer = None
        self.log_mode = 1

    def set_number_of_vehicles(self, my_number):
        self.number_of_vehicles = my_number

    def get_network(self):
        return self.network

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
