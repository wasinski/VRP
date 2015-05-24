class Algorithm(object):

    def __init__(self):
        pass

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
    def __init__(self, problem_instance, iterations=100):
        self.current_solution = problem_instance
        self.best_solution = None
        self.iterations = iterations


if __name__ == '__main__':
    pass
