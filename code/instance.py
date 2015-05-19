# TODO: add checking if route/node is fisible!
from code.datamapping import DataMapper


class ProblemInstance(object):

    def __init__(self, data_mapper):
        self.name = data_mapper.info['NAME']
        self.description = data_mapper.info['COMMENT']
        self.type = data_mapper.info['TYPE']
        self.network = data_mapper.network
        self.fleet = data_mapper.fleet
        self.distance_matrix = data_mapper.distance_matrix
        self.drawer = None
        self.log_mode = 1

    def append_vehicle(self, vehicle):
        self.fleet.append_vehicle(vehicle)

    def get_network(self):
        return self.network

    def get_node_coordinates(self):
        pass

    def get_distance_matrix(self):
        return self.distance_matrix

    def get_demand_array(self):
        pass

    def get_problem_info(self):
        return (self.name, self.type, self.description)

    def get_vehicle(self, id_):
        return self.fleet.get_vehicle(id_)
