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
            print(self.tabu)
            swap = self.generate_best_possible_swap()
            if swap is None:
                print("No swaps found - ending iterations!")
                break
            node_id, source_vehicle, dest_vehicle, position = swap
            self.perform_move(node_id, source_vehicle, dest_vehicle, position)
            if self.instance.value < self.best_instance.value:
                self.best_instance = copy.deepcopy(self.instance)
            if len(self.tabu) > 8:
                self.tabu.pop(0)
            self.iterations -= 1

    def perform_move(self, node_id, source_vehicle, dest_vehicle, position):
        self.instance.value
        print("before:")
        for vehicle in self.instance.solution.fleet:
            for node in vehicle.route:
                print(node.id, end=", ")
            print("\n")
        node = source_vehicle.route.pop_node_id(node_id)
        dest_vehicle.route.insert_node(position, node)
        self.instance.value = self.instance.eval()
        self.tabu.append(node_id)
        print("\nafter:")
        for vehicle in self.instance.solution.fleet:
            for node in vehicle.route:
                print(node.id, end=", ")
            print("\n")

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
        edges = []
        for vehicle in self.instance.solution.fleet:
            edges.extend(self.get_sorted_edges(vehicle))
        edges = sorted(edges, reverse=False, key=lambda edge: self.instance.distance_between(edge[0], edge[1]))

        chosen_swap = None
        while(edges):
            longest_edge = list(edges.pop())
            for node_id in longest_edge:
                if node_id is DEPOT:
                    longest_edge.remove(node_id)
            for node_id in longest_edge:
                if node_id is DEPOT:
                    longest_edge.remove(node_id)
            if longest_edge:
                for node_id in longest_edge:
                    neighbours = self.best_neighbours(node_id)
                    while neighbours:
                        neighbour_id = neighbours.pop()[0]
                        source_vehicle = self.instance.solution.fleet.search_for_node(node_id)
                        dest_vehicle = self.instance.solution.fleet.search_for_node(neighbour_id)
                        position = dest_vehicle.route.get_node_position(neighbour_id)
                        if self.assess_move(node_id, source_vehicle, dest_vehicle, position):
                            if node_id in self.tabu:
                                if self.check_aspiration_criteria(node_id, source_vehicle, dest_vehicle, position):
                                    chosen_swap = (node_id, source_vehicle, dest_vehicle, position)
                                    return chosen_swap
                            else:
                                chosen_swap = (node_id, source_vehicle, dest_vehicle, position)
                                return chosen_swap
                        elif self.assess_move(node_id, source_vehicle, dest_vehicle, position+1):
                            if node_id in self.tabu:
                                if self.check_aspiration_criteria(node_id, source_vehicle, dest_vehicle, position+1):
                                    chosen_swap = (node_id, source_vehicle, dest_vehicle, position+1)
                                    return chosen_swap
                            else:
                                chosen_swap = (node_id, source_vehicle, dest_vehicle, position+1)
                                return chosen_swap
        return chosen_swap

    def check_aspiration_criteria(self, node_id, source_vehicle, dest_vehicle, position):
        instance_value = self.instance.value

        source_route_value = self.instance.route_value(source_vehicle)
        dest_route_value = self.instance.route_value(dest_vehicle)
        new_src_val = self.instance.route_value_without(source_vehicle, node_id)
        new_dest_val = self.instance.route_value_with_extra(dest_vehicle, node_id, position)

        diminished_value = instance_value - (source_route_value + dest_route_value)
        new_instance_value = diminished_value + (new_src_val + new_dest_val)
        return (new_instance_value < instance_value)

    def assess_move(self, node_id, source_vehicle, dest_vehicle, position):
        if not self.check_move_feasibility(dest_vehicle, node_id):
            return False
        if len(dest_vehicle.route.route) < position or position is 0:
            return False
        source_route_value = self.instance.route_value(source_vehicle)
        dest_route_value = self.instance.route_value(dest_vehicle)
        new_src_val = self.instance.route_value_without(source_vehicle, node_id)
        new_dest_val = self.instance.route_value_with_extra(dest_vehicle, node_id, position)
        return (new_src_val + new_dest_val < source_route_value + dest_route_value)

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
        edges = sorted(edges, reverse=False, key=lambda edge: self.instance.distance_between(edge[0], edge[1]))
        return edges

    def check_move_feasibility(self, vehicle, node_id):
        if vehicle.route.get_node_position(node_id):
            return False
        demand = self.instance.solution.network.get_node(node_id).demand
        vehicle.update_load()
        return (vehicle.load + demand < vehicle.capacity)
