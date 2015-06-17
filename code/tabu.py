import copy

DEPOT = 1


class TabuSearch(object):

    def __init__(self, instance, iterations):
        self.tabu = []
        # self.instance = instance
        # self.best_instance = copy.deepcopy(instance)  # copy do zrobienia
        # self.best_value = self.best_instance.eval()
        # self.iterations = iterations

    def run(self):
        while self.iterations > 0:
            pass
            self.iterations -= 1

    def optimize_internal(self):
        for vehicle in self.instance.fleet:
            vehicle.route
            pass  # tak tak...

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
        print(dest_route)
        if position is None:
            position = len(dest_route) - 1
        if node_id is DEPOT:
            raise ValueError
        swap_node = source_route.pop_node_id(node_id)
        dest_route.insert_node(position, swap_node)
        return dest_route

    def choose_edge(self):
        pass

    def eval(self):
        self.check_feasibility()
        self.calculate_value()

    def check_feasibility(self):
        pass

    def calculate_value(self):
        pass


class ParallelTS(object):
    pass
