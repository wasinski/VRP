import copy

DEPOT = 1


class TabuSearch(object):

    def __init__(self, instance):
        self.tabu = []
        self.instance = instance
        self.current_best = copy.deepcopy(instance)  # copy do zrobienia
        self.best_value
        self.iterations

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

    def swap_2opt(self, route, i, k):
        new_route = []
        pass

    def swap_intra(self, source_route, dest_route, node, position):
        pass

    def choose_edge(self):
        pass

    def eval(self):
        check_feasibility()
        calculate_value()

    def check_feasibility(self):
        pass

    def calculate_value(self):
        pass



class ParallelTS(object):
    pass
