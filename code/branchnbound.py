import collections
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

    def initialize(self, someArguments):
        pass

    def run(self):
        # this is just a sketch
        while self.partial_solutions:
            promising_solution = self.pop_most_promising_solution()
            self.partial_solutions.extend(promising_solution.branch())
            self.evaluate_solution_space()
            self.prune_solution_space()

    def branch(self, edge):
        pass

    def pop_most_promising_solution(self):
        most_promising = self.partial_solutions[0]
        index = 0
        for i, solution in enumerate(self.partial_solutions):
            if self.is_more_promising(most_promising, solution):
                most_promising = solution
                index = i
        return self.partial_solutions.pop(index)

    def prune(self):
        pass

    def is_more_promising(self, best, current):
        if current.lower_bound <= best.lower_bound:
            if len(current.edges[True]) > len(best.edges[True]):
                return True
        else:
            return False


class BnBPartialSolution(object):

    def __init__(self, partial_solution):
        self.network = copy.deepcopy(partial_solution.network, memo={})
        self.routes = copy.deepcopy(partial_solution.routes, memo={})
        self.distance_matrix = partial_solution.distance_matrix.copy()
        self.lower_bound = partial_solution.lower_bound
        self.edges = copy.deepcopy(partial_solution.edges, memo={})
        self.is_feasible = partial_solution.is_feasible
        self.unsolvable = partial_solution.unsolvable

    @classmethod
    def init_from_instance(cls, instance):
        cls.network = instance.network
        cls.routes = None
        cls.distance_matrix = BnBPartialSolution.convert(instance.distance_matrix, len(instance.fleet))
        cls.lower_bound = None
        cls.edges = {True: [], False: []}
        cls.is_feasible = False
        cls.unsolvable = False
        return cls(cls)

    def bound(self):
        matrix = self.distance_matrix
        row_minimums = matrix[1:, 1:].min(axis=1)
        row_minimums = row_minimums[:, np.newaxis]
        matrix[1:, 1:] -= row_minimums
        column_minimums = matrix[1:, 1:].min(axis=0)
        matrix[1:, 1:] -= column_minimums
        lower_bound = sum(row_minimums) + sum(column_minimums)
        return lower_bound

    def with_edge_branch(self, edge):
        self.edges[True].append(edge)
        matrix = self.distance_matrix
        i, j = self.edge_to_real_indexes(edge)
        matrix = np.delete(matrix, (i), axis=0)
        matrix = np.delete(matrix, (j), axis=1)

    def without_edge_branch(self, edge):
        self.edges[False].append(edge)
        matrix = self.distance_matrix
        i, j = self.edge_to_real_indexes(edge)
        matrix[i, j] = float("inf")
        self.evaluate_solution()

    def is_leaf(self):
        pass

    def solve_leaf(self):
        pass

    def evaluate_solution(self):
        pass

    def check_feasibility(self):
        pass

    def routes_edges_to_nodes(self):
        DEPOT = 1
        converted_routes = []
        for route in self.routes:
            converted_route = []
            for edge in route:
                entry, exit = edge
                if entry not in converted_route:
                    converted_route.append(entry)
                if exit not in converted_route or exit is DEPOT:
                    converted_route.append(exit)
            converted_routes.append(converted_route)
        return converted_routes

    def edge_to_real_indexes(self, edge):
        row, column = edge
        real_row = None
        real_column = None
        for i, row_index in enumerate(self.distance_matrix[:, 0]):
            if row == row_index:
                real_row = i
                break
        for j, col_index in enumerate(self.distance_matrix[0, :]):
            if column == col_index:
                real_column = j
                break
        if real_row is None or real_column is None:
            raise ValueError
        return (real_row, real_column)

    def construct_routes(self):
        DEPOT = 1
        routes = []
        edges = collections.deque(self.edges[True])
        memo = {}
        routes.append([edges.pop()])
        while edges:
            edge = edges.pop()
            inserted = False
            for route in routes:
                for i, route_edge in enumerate(route):
                    if edge[1] == route_edge[0] and edge[1] is not DEPOT:
                        if i == 0 or route[i - 1][1] == edge[0]:
                            route.insert(i, edge)
                            inserted = True
                            break
                    elif route_edge[1] == edge[0] and edge[0] is not DEPOT:
                        if (i == len(route) - 1) or edge[1] == route[i + 1][0]:
                            route.insert(i + 1, edge)
                            inserted = True
                            break
            if not inserted:
                try:
                    memo[edge] += 1
                    if memo[edge] > 2:
                        routes.append([edge])
                    else:
                        edges.appendleft(edge)
                except KeyError:
                    memo[edge] = 1
                    edges.appendleft(edge)

        # until begins/ends (and that's possible) in depot rotate route
        """for route in routes:
            normalizable = False
            for edge in route:
                if edge[0] is DEPOT or edge[1] is DEPOT:
                    normalizable = True
            if normalizable:
                normalized = False
                while not normalized:
                    if route[0][0] is DEPOT or route[-1][1] is DEPOT:
                        normalized = True
                    else:
                        route.insert(0, route.pop())
            else:
                continue"""
        self.routes = routes

    def select_edge(self):
        matrix = self.distance_matrix
        best_edge = (None, None)
        highest_penalty = 0
        for i in range(1, len(matrix)):
            for j in range(1, len(matrix)):
                if matrix[i, j] is 0:
                    continue
                row = matrix[i, 1:].copy()
                row[j-1] = float("inf")
                column = matrix[1:, j].copy()
                column[i-1] = float("inf")
                penalty = min(row) + min(column)
                if penalty > highest_penalty:
                    row_index = matrix[i, 0]
                    col_index = matrix[0, j]
                    highest_penalty = penalty
                    best_edge = (row_index, col_index)

        return best_edge

    def convert(matrix, fleet_size):
        converted = []
        # TODO: I actually wonder if it wasn't been better to work on the np.array from the beginning...
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
