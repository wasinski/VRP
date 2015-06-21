import collections
import numpy as np
import copy
# TODO: byc moze trzeba bedzie dopracowac is_feasible zeby sprawdzalo
# czy sciezki są unikatowe

DEPOT = 1


class BranchNBound(object):
    """ Branch and bound implementation

        This algorithm uses m-TSP relaxation and BnB method proposed by Little et. al.
        Additionally routes for every vehicle are constructed at end of every iteration
            and solutions that wont be feasible are detected, and pruned.
    """
    def __init__(self):
        self.partial_solutions = []
        self.upper_bound = None
        self.current_best = None
        self.times_branched = 0
        self.initial_upper_bound = None

    def initialize(self, instance, upper_bound=None):
        first_partial = BnBPartialSolution.init_from_instance(instance)
        first_partial.bound()
        self.upper_bound = upper_bound
        self.initial_upper_bound = upper_bound
        self.current_best = first_partial
        self.partial_solutions.append(first_partial)

    def run(self):
        while self.partial_solutions:
            promising_solution = self.pop_most_promising_solution()
            if promising_solution.remove:
                print("removing!")
                continue
            print("pp, lowerb: "+ str(promising_solution.lower_bound))
            print("pp, edges: ")
            print(str(promising_solution.edges))
            print("pp, matrix: ")
            print(str(promising_solution.distance_matrix))
            self.branch(promising_solution)
            self.prune()
            print("-----------------------")
        return (self.upper_bound, self.current_best.routes, self.current_best.edges[True], self.times_branched)

    def branch(self, to_branch):
        best_edge = to_branch.select_edge()
        if None in best_edge:
            return
        # left, with-branch
        left_solution = BnBPartialSolution.init_from_partial(to_branch)
        left_solution.with_edge_branch(best_edge)
        if left_solution.is_acceptable(self.upper_bound):
            self.partial_solutions.append(left_solution)

        # right, without-branch
        right_solution = BnBPartialSolution.init_from_partial(to_branch)
        right_solution.without_edge_branch(best_edge)
        if right_solution.is_acceptable(self.upper_bound):
            self.partial_solutions.append(right_solution)

        self.times_branched += 1

    def pop_most_promising_solution(self):
        most_promising = self.partial_solutions[0]
        index = 0
        for i, solution in enumerate(self.partial_solutions):
            if self.is_more_promising(most_promising, solution):
                most_promising = solution
                index = i
        return self.partial_solutions.pop(index)

    def prune(self):
        for solution in self.partial_solutions:

            if solution.lower_bound >= self.upper_bound:
                solution.remove = True
                continue

            if solution.is_feasible is False:
                solution.remove = True
                continue

            if solution.leaf:
                first_solution = BnBPartialSolution(solution)
                second_solution = BnBPartialSolution(solution)
                solution.remove = True
                try:
                    first_solution.solve_leaf_first()
                    first_solution.construct_routes()
                    first_solution.set_is_feasible(final=True)

                    if first_solution.is_feasible:
                        value = first_solution.calculate_value()
                        if value < self.upper_bound:
                            self.upper_bound = value
                            self.current_best = first_solution
                except ValueError:
                    pass
                try:
                    second_solution.solve_leaf_second()
                    second_solution.construct_routes()
                    second_solution.set_is_feasible(final=True)

                    if second_solution.is_feasible:
                        value = second_solution.calculate_value()
                        if value < self.upper_bound:
                            self.upper_bound = value
                            self.current_best = second_solution
                except ValueError:
                    pass

                continue

    def is_more_promising(self, best, current):
        if current.lower_bound <= best.lower_bound:
            if len(current.edges[True]) > len(best.edges[True]):
                return True
        else:
            return False


class BnBPartialSolution(object):

    def __init__(self, instance):
        self.lookup_matrix = instance.lookup_matrix
        self.network = instance.network
        self.routes = instance.routes
        self.distance_matrix = instance.distance_matrix
        self.lower_bound = instance.lower_bound
        self.edges = instance.edges
        self.is_feasible = instance.is_feasible
        self.leaf = instance.leaf
        self.capacity = instance.capacity
        self.remove = instance.remove

    @classmethod
    def init_from_instance(cls, instance):
        cls.lookup_matrix = np.array(instance.distance_matrix)
        cls.network = instance.network
        cls.routes = None
        cls.distance_matrix = BnBPartialSolution.convert(instance.distance_matrix, len(instance.fleet))
        cls.lower_bound = None
        cls.edges = {True: [], False: []}
        cls.is_feasible = True
        cls.leaf = False
        cls.capacity = instance.fleet.fleet[0].capacity
        cls.remove = False
        return cls(cls)

    @classmethod
    def init_from_partial(cls, partial):
        cls.lookup_matrix = partial.lookup_matrix
        cls.network = partial.network
        cls.routes = None
        cls.distance_matrix = partial.distance_matrix.copy()
        cls.lower_bound = partial.lower_bound
        cls.edges = copy.deepcopy(partial.edges)
        cls.is_feasible = partial.is_feasible
        cls.leaf = partial.leaf
        cls.capacity = partial.capacity
        cls.remove = partial.remove
        return cls(cls)

    def is_acceptable(self, upper_bound):
        if self.is_feasible is True:
            if self.lower_bound < upper_bound:
                return True
        return False

    def bound(self):
        matrix = self.distance_matrix
        row_minimums = matrix[1:, 1:].min(axis=1)
        row_minimums = row_minimums[:, np.newaxis]
        for i, minimum in enumerate(row_minimums):
            if minimum == float("inf"):
                row_minimums[i] = 0
        matrix[1:, 1:] -= row_minimums
        column_minimums = matrix[1:, 1:].min(axis=0)
        for i, minimum in enumerate(column_minimums):
            if minimum == float("inf"):
                column_minimums[i] = 0
        matrix[1:, 1:] -= column_minimums
        lower_bound = float(sum(row_minimums) + sum(column_minimums))
        try:
            self.lower_bound += lower_bound
        except TypeError:
            self.lower_bound = lower_bound
        return lower_bound

    def with_edge_branch(self, edge):
        reversed_edge = (edge[1], edge[0])
        self.edges[True].append(edge)
        matrix = self.distance_matrix
        i, j = self.edge_to_real_indexes(edge)[0]
        matrix = np.delete(matrix, (i), axis=0)
        matrix = np.delete(matrix, (j), axis=1)
        self.distance_matrix = matrix
        if DEPOT not in reversed_edge:
            if self.set_infinities(reversed_edge):
                self.edges[False].append(reversed_edge)

        if self.is_leaf():
            self.leaf = True

        self.construct_routes()
        self.prevent_revisiting()
        self.bound()
        self.set_is_feasible()

    def without_edge_branch(self, edge):
        if self.set_infinities(edge):
            self.edges[False].append(edge)
        self.bound()

    def is_leaf(self):
        if len(self.distance_matrix) is 3:
            return True
        elif len(self.distance_matrix) < 3:
            raise ValueError
        else:
            return False

    def solve_leaf_first(self):
        matrix = self.distance_matrix

        edge1 = (int(matrix[1, 0]), int(matrix[0, 1]))
        edge2 = (int(matrix[2, 0]), int(matrix[0, 2]))

        if edge1[0] == edge1[1] or edge2[0] == edge2[1]:
            raise ValueError
        else:
            if edge1 not in self.edges[True]:
                self.edges[True].append(edge1)
            if edge2 not in self.edges[True]:
                self.edges[True].append(edge2)

    def solve_leaf_second(self):
        matrix = self.distance_matrix

        edge1 = (int(matrix[1, 0]), int(matrix[0, 2]))
        edge2 = (int(matrix[2, 0]), int(matrix[0, 1]))

        if edge1[0] == edge1[1] or edge2[0] == edge2[1]:
            raise ValueError
        else:
            if edge1 not in self.edges[True]:
                self.edges[True].append(edge1)
            if edge2 not in self.edges[True]:
                self.edges[True].append(edge2)

    def calculate_value(self):
        routes = self.routes_edges_to_nodes()
        distance = 0
        for route in routes:
            for i, node_id in enumerate(route):
                try:
                    source_id = node_id
                    destination_id = route[i + 1]
                except IndexError:
                    break
                distance += self.distance_between(source_id, destination_id)
        return distance

    def distance_between(self, source_id, destination_id):
        return self.lookup_matrix[source_id - 1, destination_id - 1]

    def prevent_revisiting(self):  # puts infinities acording to the algo.
        routes = self.routes_edges_to_nodes()
        for route in routes:
            if len(route) < 3:
                continue  # 2 element routes should be delt sooner.

            edge = (route[-1], route[0])
            if DEPOT not in edge:
                if self.set_infinities(edge):
                    self.edges[False].append(edge)

    def set_is_feasible(self, final=False):  # i.e. it doesn't already break the constraints (capacity)
        routes_nodes = self.routes_edges_to_nodes()
        for route in routes_nodes:
            load = 0
            for node_id in route:
                load += self.network.get_node(node_id).demand
                if load > self.capacity:
                    self.is_feasible = False
        if final:
            for route in routes_nodes:
                if route[0] is not DEPOT or \
                    route[-1] is not DEPOT:
                    self.is_feasible = False

    def set_infinities(self, edge):
        matrix = self.distance_matrix
        real_edges = self.edge_to_real_indexes(edge)
        set_ = False
        for i, j in real_edges:
            matrix[i, j] = float("inf")
            set_ = True
        self.distance_matrix = matrix
        return set_

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
        real_row = []
        real_column = []
        real_edges = []
        for i, row_index in enumerate(self.distance_matrix[:, 0]):
            if row == row_index:
                real_row.append(i)
        for j, col_index in enumerate(self.distance_matrix[0, :]):
            if column == col_index:
                real_column.append(j)

        for row_idx in real_row:
            for col_idx in real_column:
                real_edges.append((row_idx, col_idx))
        return real_edges

    def construct_routes(self):
        routes = []
        edges = copy.deepcopy(self.edges[True])

        route = []
        route.append(edges.pop())
        found_match = True
        while True:
            found_match = False
            on_start = None
            index = None
            end = route[-1][1]
            start = route[0][0]

            for i, edge in enumerate(edges):
                if edge[0] == end and end is not DEPOT:
                    found_match = True
                    on_start = False
                    index = i
                elif edge[1] == start and start is not DEPOT:
                    found_match = True
                    on_start = True
                    index = i

            if found_match:
                edge = edges.pop(index)
                if on_start:
                    route.insert(0, edge)
                else:
                    route.append(edge)
            else:
                routes.append(route)
                route = []
                try:
                    route.append(edges.pop())
                except IndexError:
                    break

        self.routes = routes

    def select_edge(self):
        matrix = self.distance_matrix
        best_edge = (None, None)
        highest_penalty = 0
        for i in range(1, len(matrix)):
            for j in range(1, len(matrix)):
                if matrix[i, j] != 0:
                    continue
                row = matrix[i, 1:].copy()
                row[j - 1] = float("inf")
                column = matrix[1:, j].copy()
                column[i - 1] = float("inf")
                penalty = min(row) + min(column)
                if highest_penalty <= penalty:
                    row_index = int(matrix[i, 0])
                    col_index = int(matrix[0, j])
                    edge = (row_index, col_index)
                    highest_penalty = penalty
                    best_edge = edge
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
