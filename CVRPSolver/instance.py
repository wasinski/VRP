from code.supports import Importer as I


class ProblemInstance(object):

    def __init__(self, my_info, my_space, my_vehicle, my_number=0):
        self.name = my_info['NAME']
        self.comment = my_info['COMMENT']
        self.type = my_info['TYPE']
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

    def __init__(self, my_node_coordinates, my_adjacency_matrix):
        self.node_coordinates = my_node_coordinates
        self.adjacency_matrix = my_adjacency_matrix


class Node(object):

    def __init__(self, my_id, my_node_coordinates, my_demand):
        self.id = my_id
        self.coordinates = my_node_coordinates
        self.demand = my_demand

    def get_demand(self):
        return self.demand

    def get_coordinates(self):
        return self.coordinates

    def get_id(self):
        return self.id


class Vehicle(object):  # TODO: add checking if route/node is fisible!

    __id = 0

    def __init__(self, my_capacity):
        self.id = Vehicle.__id
        Vehicle.__id += 1
        self.capacity = my_capacity
        self.route = []

    def set_route(self, my_route):
        self.route = my_route

    def set_route_add_node(self, my_node):
        self.route.append(my_node)

    def get_capacity(self):
        return self.capacity

    def get_route(self):
        return self.route
