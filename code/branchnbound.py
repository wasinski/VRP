class BranchNBound(object):

    def __init__(self, instance):
        self.partial_solutions = []
        self.upper_bound = None
        self.current_best = None

    def bound(self):
        pass

    def branch(self):
        pass

    def run(self):
        pass


class BnBPartialSolution(object):

    def __init__(self, instance):
        self.solution = None
        self.lower_bound = None
        self.edges = {True: [], False: []}

    def construct_route(self):
        pass


"""
ok, więc na wstępie potrzebuję odpowiednich struktur z możliwością ich kopiowania:
    instancja problemu rozszerzona"""
