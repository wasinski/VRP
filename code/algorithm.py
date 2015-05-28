from code import instance


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
        pass

if __name__ == '__main__':
    pass
