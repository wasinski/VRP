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
            instance_memo = copy.deepcopy(self.instance)
            node_id = self.optimize_intra()

            self.instance.value = self.instance.eval()
            if self.instance.value < self.best_instance.value:
                self.best_instance = copy.deepcopy(self.instance)
                print("found better!")
                if node_id not in self.tabu:
                    self.tabu.append(node_id)
            else:
                if node_id in self.tabu:
                    print("caly czas tluklo")
                    print(node_id)
                    self.instance = instance_memo
                    reasses = True
                else:
                    self.tabu.append(node_id)
            if len(self.tabu) > 8:
                self.tabu.pop(0)
            self.iterations -= 1

    def optimize(self):
        pass

    def optimize_intra(self, reasses=False):
        source_vehicle_id, node_id = self.choose_node(tabu=reasses)
        dest_vehicle_id, neighbor_id = self.generate_best_possible_swap(node_id)
        if source_vehicle_id is None or node_id is None or dest_vehicle_id is None or neighbor_id is None:
            return None
        source_vehicle = self.instance.solution.fleet.get_vehicle(source_vehicle_id)
        dest_vehicle = self.instance.solution.fleet.get_vehicle(dest_vehicle_id)
        neighbor_position = dest_vehicle.route.get_node_position(neighbor_id)

        self.swap_intra(source_vehicle.route, dest_vehicle.route, node_id, neighbor_position)

        return node_id


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

    def swap_intra(self, source_route, dest_route, node_id, position=None):
        if position is None:
            position = len(dest_route) - 1
        if node_id is DEPOT:
            raise ValueError
        swap_node = source_route.pop_node_id(node_id)
        dest_route.insert_node(position, swap_node)
        return dest_route

    def generate_best_possible_swap(self, node_id):
        closest = float("inf")
        vehicle_id = None
        neighbor_id = None
        for vehicle in self.instance.solution.fleet:
            for node in vehicle.route:
                distance = self.instance.distance_between(node.id, node_id)
                if distance < closest:
                    if self.instance.solution.network.get_node(node_id).demand + vehicle.load <= vehicle.capacity:
                        closest = distance
                        vehicle_id = vehicle.id
                        neighbor_id = node.id
        return (vehicle_id, neighbor_id)

    def choose_node(self, longest=0, tabu=False):  # this is bad and wrong, and evil
        longest = 0
        edge = None
        vehicle_id = None
        for vehicle in self.instance.solution.fleet:
            for i, node in enumerate(vehicle.route):
                if tabu:
                    if node.id in self.tabu:
                        continue
                try:
                    distance = self.instance.distance_between(node.id, vehicle.route[i+1].id)
                except IndexError:
                    break
                if longest < distance:
                    longest = distance
                    edge = (node.id, vehicle.route[i+1].id)
                    vehicle_id = vehicle.id

        if edge[1] is DEPOT:
            return (vehicle_id, edge[0])
        else:
            return (vehicle_id, edge[1])

    def choose_node_in_route(self, vehicle):
        edges = [(1, 1)]
        for i, node in enumerate(vehicle.route[1:]):
            edge = (vehicle.route[i-1].id, node.id)
            distance = self.instance.distance_between(edge[0], edge[1])
            if distance > self.instance.distance_between(edges[-1][0], edges[-1][1]):
                edges.append(edge)
        edges.pop(0)
        for edge in reversed(edges):
            if edge[0] is not DEPOT and edge[1] is not DEPOT:
                return edge
        return None

