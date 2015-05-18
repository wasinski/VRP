import numpy
from code import baseobjects as bo
from code.supports import euclidian_distance, retrieve_minimal_fleet_size
from collections import deque


class Importer(object):

    def __init__(self):
        self.file_lines = []
        self.info = {}
        self.node_coordinates_list = []
        self.distance_matrix = None
        self.demand_array = None

    def import_data(self, filename):
        # do ostrego przepisania jest ta metoda, uwaga by się nie jebnąć!
        self._read_file(filename)
        self.info, break_lines = self._read_info()
        self.node_coordinates_list, demand_list = \
            self._return_nodes_and_delivery_lists(break_lines)
        adjacency_matrix_list = \
            self._create_distance_matrix(self.node_coordinates_list, int(self.info["DIMENSION"]))

        self.distance_matrix = numpy.array(adjacency_matrix_list)
        self.demand_array = numpy.array(demand_list)

    def _read_file(self, my_filename):
        filelines = []
        with open(my_filename, "rt") as f:
            filelines = f.read().splitlines()
        self.file_lines = filelines

    def _read_info(self):

        my_filelines = self.file_lines
        info = {}
        start = 0
        middle = 0
        end = 0

        for i, line in enumerate(my_filelines):
            if line.startswith("NODE_COORD_SECTION"):
                start = i
            elif line.startswith("DEMAND_SECTION"):
                middle = i
            elif line.startswith("DEPOT_SECTION"):
                end = i
            elif line.startswith("EOF"):
                break
            elif line.split(' ')[0].isupper():  # checks if line begins with UPPERCASE key
                splited = line.split(':')
                info[splited[0].strip()] = splited[1].strip()

        return info, (start, middle, end)

    def _return_nodes_and_delivery_lists(self, my_breaklines):
        my_filelines = self.file_lines
        start, middle, end = my_breaklines
        node_coordinates_list = []
        demand_list = []

        for i, line in enumerate(my_filelines):
            if start < i < middle:
                splited = line.split(' ')
                splited = list(map(float, splited))
                node_coordinates_list.append((splited[1], splited[2]))

            if middle < i < end:
                splited = line.split(' ')
                splited = list(map(int, splited))
                demand_list.append(splited[1])

        return node_coordinates_list, demand_list

    def _create_distance_matrix(self, my_node_coordinates_list, my_dimension):
        ncl = deque(my_node_coordinates_list[:])
        matrix = []
        while ncl:
            row = [0] * (my_dimension + 1 - len(ncl))
            node1 = ncl.popleft()
            for node2 in ncl:
                row.append(euclidian_distance(node1, node2))
            matrix.append(row)

        for i in range(my_dimension):  # mirroring the matrix
            for j in range(my_dimension):
                try:
                    matrix[j][i] = matrix[i][j]
                except IndexError as e:
                    print("##ERROR!##\nBad indexing: " + str((i, j)))
                    print("that definitly shouldnt happen, it >might< be a problem with the imported file")
                    raise e

        return matrix


class DataMapper(object):

    def __init__(self, my_importer):
        minimal_fleet_size = retrieve_minimal_fleet_size(my_importer.info["NAME"])
        self.info = my_importer.info
        self.network = self._create_network(my_importer.node_coordinates_list, my_importer.demand_array)
        self.fleet = self._create_fleet(my_importer.info["CAPACITY"], minimal_fleet_size)
        self.distance_matrix = my_importer.distance_matrix

    def _create_network(self, node_coordinates_list, demand_array):
        network = bo.Network()
        for id_, (node_coords, demand) in enumerate(zip(node_coordinates_list, demand_array)):
            node = bo.Node(id_, node_coords, demand)
            network.append_node(node)
        return network

    def _create_fleet(self, capacity, number_of_vehicles=0):
        vehicles_left = int(number_of_vehicles)
        fleet = bo.Fleet()
        while (vehicles_left):
            vehicle = bo.Vehicle(capacity)
            fleet.append_vehicle(vehicle)
            vehicles_left -= 1
        return fleet
