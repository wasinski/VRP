import copy
DEPOT = 1


class Algorithm(object):

    def __init__(self, iterations, algo):
        self.iterations = iterations
        self.algo = algo

    def initialize(self):
        pass

    def iterate(self):
        pass


class Solution(object):
    """wstępnie - lista id nodów,
        metody is_feasable i calculate,
        zawiera: current solution (problem instance)
                 best solution(problem instance)
                 best_fitness

        zastanowić się czy metody calculate i is_feasable nie byłby lepsze w Problem Instance.
        wtedy: solution służyłoby tylko za kontener na którym pracowałby algorithm z odpowiednim
        algorithmem ;)
    """
    def __init__(self, problem_instance):
        self.solution = problem_instance
        self.feasible = False
        self.value = None

    def eval(self):
        if self.is_feasible():
            self.feasible = True
            return self.calculate_value()
        else:
            self.feasible = False
            return None

    def is_feasible(self):
        for vehicle in self.solution.fleet:
            if vehicle.route[0].id is not DEPOT or vehicle.route[-1].id is not DEPOT:
                return False
        return True

    def calculate_value(self):
        summary_distance = 0
        for vehicle in self.solution.fleet:
            summary_distance += self.route_value(vehicle)
        return summary_distance

    def route_value(self, vehicle):
        vehicle_distance = 0
        for i, node in enumerate(vehicle.route):
            try:
                source_id = node.id
                destination_id = vehicle.route[i+1].id
            except IndexError:
                break
            vehicle_distance += self.distance_between(source_id, destination_id)
        return vehicle_distance

    def route_value_with_extra(self, vehicle, node_id, position):
        temp_vehicle = copy.deepcopy(vehicle)
        node = self.solution.network.get_node(node_id)
        temp_vehicle.route.insert_node(position, node)
        return self.route_value(temp_vehicle)

    def route_value_without(self, vehicle, node_id):
        temp_vehicle = copy.deepcopy(vehicle)
        temp_vehicle.route.pop_node_id(node_id)
        return self.route_value(temp_vehicle)


    def distance_between(self, source_id, destination_id):
        return self.solution.distance_matrix[source_id-1][destination_id-1]

if __name__ == '__main__':
    pass
