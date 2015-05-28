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

    def evaluate(self):
        pass

    def is_feasible(self):
        pass

    def calculate_value(self):
        summary_distance = 0
        for vehicle in self.solution.fleet:
            vehicle_distance = 0
            for i, node in enumerate(vehicle.route):
                try:
                    source_id = node.id
                    destination_id = vehicle.route[i+1].id
                except IndexError:
                    break
                vehicle_distance += self.distance_between(source_id, destination_id)
            summary_distance += vehicle_distance
        return summary_distance

    def distance_between(self, source_id, destination_id):
        return self.solution.distance_matrix[source_id-1][destination_id-1]

if __name__ == '__main__':
    pass
