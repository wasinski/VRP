import numpy as np
import copy


class BranchNBound(object):
    """ Branch and bound implementation

        This algorithm uses m-TSP relaxation and BnB method proposed by Little et. al.
        Additionally routes for every vehicle are constructed at end of every iteration
            and solutions that wont be feasible are detected, and pruned.
    """
    def __init__(self, instance):
        self.partial_solutions = []
        self.upper_bound = None
        self.current_best = None
        self.times_branched = 0
        self.initial_upper_bound = None

    def run(self):
        pass

    def select_most_promising(self):
        pass

    def prune(self):
        pass


class BnBPartialSolution(object):

    def __init__(self, partial_solution):
        self.network = copy.deepcopy(partial_solution.network, memo={})
        self.fleet = copy.deepcopy(partial_solution.fleet, memo={})
        self.distance_matrix = copy.deepcopy(partial_solution.distance_matrix)
        self.lower_bound = partial_solution.lower_bound
        self.edges = copy.deepcopy(partial_solution.edges, memo={})

    @classmethod
    def init_from_instance(cls, instance):
        cls.network = instance.network
        cls.fleet = instance.fleet
        cls.distance_matrix = BnBPartialSolution.convert(instance.distance_matrix, len(instance.fleet))
        cls.lower_bound = None
        cls.edges = {True: [], False: []}
        return cls(cls)

    def compute_bound(self):
        pass

    def branch(self):
        pass

    def construct_route(self):
        pass

    def update_solution(self):
        pass

    def convert(matrix, fleet_size):
        converted = []

        # initialize matrix
        for i in range(len(matrix) + fleet_size):
            row = [float("inf")] * (len(matrix) + fleet_size)
            converted.append(row)

        # please remember that first $fleet_size rows are index = 1, and contain 'to depot' distance
        # make first row an index row
        for i in range(1, len(converted[0])):
            if i <= fleet_size:
                converted[0][i] = 1
            else:
                converted[0][i] = i - fleet_size + 1

        # make first column an index column
        for i in range(1, len(converted)):
            if i <= fleet_size:
                converted[i][0] = 1
            else:
                converted[i][0] = i - fleet_size + 1

        # seting depot distance for columns
        for i in range(1, fleet_size + 1):
            matrix_item = 1
            for j in range(fleet_size + 1, len(converted[i])):
                converted[i][j] = float(matrix[0][matrix_item])
                matrix_item += 1

        # seting depot distance for rows
        for j in range(1, fleet_size + 1):
            matrix_row = 1
            for i in range(fleet_size + 1, len(converted[i])):
                converted[i][j] = float(matrix[matrix_row][0])
                matrix_row += 1

        # copying the rest of the values
        matrix_row = 1
        for i in range(fleet_size + 1, len(converted)):
            matrix_item = 1
            for j in range(fleet_size + 1, len(converted[i])):
                converted[i][j] = float(matrix[matrix_row][matrix_item])
                if i == j:
                    converted[i][j] = float("inf")
                matrix_item += 1
            matrix_row += 1

        return np.array(converted)
