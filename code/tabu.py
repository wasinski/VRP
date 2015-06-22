import copy
from code import baseobjects as bo

DEPOT = 1


class TabuSearch(object):

    def __init__(self, solution, iterations):
        self.tabu = []
        self.instance = solution
        self.best_instance = copy.deepcopy(self.instance)  # copy do zrobienia
        self.iterations = iterations

    def run(self):
        while self.iterations > 0:
            self.optimize_intra()
            self.optimize_internal()
            self.iterations -= 1

    def optimize_internal(self):
        for vehicle in self.instance.solution.fleet:
            optimized = True
            while optimized:
                best_distance = self.instance.route_value(vehicle)
                for node1 in vehicle.route[1:-2]:
                    for node2 in vehicle.route[1:-2]:
                        try:
                            temp_route = self.swap_2opt(vehicle.route, node1.id, node2.id)
                        except ValueError:
                            continue
                        new_vehicle = copy.deepcopy(vehicle)
                        new_route = bo.Route()
                        new_route.set_route(temp_route)
                        new_vehicle.set_route(new_route)
                        new_distance = self.instance.route_value(new_vehicle)
                        if new_distance < best_distance:
                            vehicle = new_vehicle
                            optimized = True
                            continue
                        else:
                            optimized = False

    def optimize_intra(self):
        for vehicle in self.instance.fleet:
            vehicle.route
            pass  # tak tak

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

    def choose_edge(self, route):
        pass
        longest = 0
        edge = None
        second_edge = None
        for i, node in enumerate(route):
            try:
                distance = self.instance.distance_between(node.id, route[i+1].id)
            except IndexError:
                break
            if longest < distance:
                longest = distance
                edge = (node.id, route[i+1].id)
                second_edge = edge
        return (second_edge[1], edge[1])

