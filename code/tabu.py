import copy
from code import baseobjects as bo
from collections import deque

DEPOT = 1


class TabuSearch(object):

    def __init__(self, solution, iterations):
        self.tabu = []
        self.instance = solution
        self.best_instance = copy.deepcopy(self.instance)  # copy do zrobienia
        self.iterations = iterations

    def run(self):
        while self.iterations > 0:
            self.instance.value = self.instance.eval()
            if self.instance.value is None:
                raise TypeError
            instance_memo = copy.deepcopy(self.instance)
            node_id = self.optimize_intra()
            self.instance.value = self.instance.eval()
            if self.instance.value is None:
                raise TypeError
            if self.instance.value == instance_memo.value:
                print("ło kurwa wiedzialem")
                raise Exception
            if self.instance.value < instance_memo.value:
                if node_id not in self.tabu:
                    self.tabu.append(node_id)
                if self.instance.value < self.best_instance.value:
                    self.best_instance = copy.deepcopy(self.instance)
                    print("found better!")
            # aspiration criteria:
            # else:
            #     #self.instance = instance_memo
            #     if node_id not in self.tabu:
            #         self.tabu.append(node_id)
            #     node_id = self.optimize_intra(fromtabu=True)
            #     if self.instance.value < self.best_instance.value:
            #         self.best_instance = copy.deepcopy(self.instance)
            #         print("found better by aspiration!")
            if len(self.tabu) > 8:
                self.tabu.pop(0)
            print("node ID")
            print(node_id)
            print (self.tabu)
            self.iterations -= 1

    def optimize(self):
        pass

    def optimize_intra(self, fromtabu=False):
        node_id = None
        wrong_nodes = []
        while node_id is None:
            source_vehicle_id, node_id = self.choose_node(wrong_nodes, fromtabu=fromtabu)
            dest_vehicle_id, neighbor_id = self.generate_best_possible_swap(node_id)
            if source_vehicle_id is None or node_id is None or dest_vehicle_id is None or neighbor_id is None:
                print([source_vehicle_id, node_id, dest_vehicle_id, neighbor_id])
                wrong_nodes.append(node_id)
                node_id = None
        source_vehicle = self.instance.solution.fleet.get_vehicle(source_vehicle_id)
        dest_vehicle = self.instance.solution.fleet.get_vehicle(dest_vehicle_id)
        neighbor_position = dest_vehicle.route.get_node_position(neighbor_id)

        print(self.instance.solution.fleet.fleet)
        self.swap_intra(self.instance.solution.fleet.get_vehicle(source_vehicle_id), self.instance.solution.fleet.get_vehicle(dest_vehicle_id), node_id, neighbor_position)
        return node_id

    def swap_intra(self, source_vehicle, dest_vehicle, node_id, position=None):
        if position is None:
            position = len(dest_vehicle.route) - 1
        if node_id is DEPOT:
            raise ValueError
        print(source_vehicle, dest_vehicle)
        print(source_vehicle.route.get_node_position(node_id), position)
        swap_node = source_vehicle.route.pop_node_id(node_id)
        dest_vehicle.route.insert_node(position, swap_node)
        print(swap_node, source_vehicle, dest_vehicle)

    def swap_2opt(self, route, i_id, k_id):
        if i_id is DEPOT or k_id is DEPOT:
            raise ValueError

        i = route.get_node_position(i_id)
        k = route.get_node_position(k_id)
        new_route = []
        new_route.extend(route[0:i])
        between = route[i:k+1]
        between.reverse()
        new_route.extend(between)
        new_route.extend(route[k+1:])
        return new_route

    def generate_best_possible_swap(self):
        for vehicle in self.instance.solution.fleet:
            edges = self.get_sorted_edges(vehicle)
            longest_edge = list(edges.pop())
            for node_id in longest_edge:
                if node_id is DEPOT:
                    longest_edge.remove(node_id)
            if longest_edge:
                for node_id in longest_edge:
                    neighbours = self.best_neighbours(node_id)


    def assess_move(self, node_id, source_vehicle, dest_vehicle, position):
        source_route_value = self.instance.route_value(source_vehicle)
        dest_route_value = self.instance.route_value(dest_vehicle)

    def best_neighbours(self, node_id):
        neighbours = []
        for pos, neighbour_dist in enumerate(self.instance.solution.distance_matrix[node_id-1]):
            neighbours.append((pos+1, neighbour_dist))
        neighbours = sorted(neighbours, reverse=True, key=lambda neighbour: neighbour[1])
        neighbours.pop()
        return neighbours

    def get_sorted_edges(self, vehicle):
        edges = []
        for i, node in enumerate(vehicle.route):
            try:
                edge = (node.id, vehicle.route[i+1].id)
                edges.append(edge)
            except IndexError:
                break
        for node in vehicle.route:
            print(node.id)
        print (edges)
        edges = sorted(edges, reverse=False, key=lambda edge: self.instance.distance_between(edge[0], edge[1]))
        return edges

