import unittest
import numpy
from code import branchnbound as bnb
from code import instance as i
from code import datamapping as dm
from code import greedyfirst as gf
from code import algorithm as a


class TestBnB(unittest.TestCase):

    def setUp(self):
        raw_data = dm.Importer()
        raw_data.import_data("./tests/cvrp2.test")
        #raw_data.import_data("./tests/E-n23-k3.vrp")
        data = dm.DataMapper(raw_data)

        self.instance = i.ProblemInstance(data)

        self.instance.distance_matrix = [
            [0, 6, 3, 1, 7, 11],
            [6, 0, 5, 9, 6, 3],
            [3, 5, 0, 8, 2, 4],
            [1, 9, 8, 0, 9, 9],
            [7, 6, 2, 9, 0, 3],
            [11,3, 4, 9, 3, 0]
        ]

        self.solution = a.Solution(self.instance)

        greedy = gf.GreedyFirst(self.solution.solution)
        greedy.run(sort=False)
        self.solution.value = self.solution.calculate_value()
        self.value = self.solution.value

    def test_run(self):
        bnb_algo = bnb.BranchNBound()
        print("starting branchNbound with initial FAKE upper bound:" + str(self.value))
        bnb_algo.initialize(self.instance, self.value+100)
        upper_bound, routes, times_branched = bnb_algo.run()

        print("times branched: " + str(times_branched))
        print("value: "+ str(upper_bound))
        print("routes: "+ str(routes))


class TestBnBPartialSolution1(unittest.TestCase):

    def setUp(self):
        raw_data = dm.Importer()
        raw_data.import_data("./tests/cvrp1.test")
        data = dm.DataMapper(raw_data)

        self.instance = i.ProblemInstance(data)

    def test_convert(self):
        entry_matrix = [
            [0, 1, 2, 3, 4],
            [1, 0, 5, 6, 7],
            [2, 5, 0, 8, 9],
            [3, 6, 8, 0, 1],
            [4, 7, 9, 1, 0]
        ]
        converted_matrix = bnb.BnBPartialSolution.convert(entry_matrix, fleet_size=2)
        master1 = [
            [float("inf"), 1., 1., 2., 3., 4., 5.],
            [1., float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [1., float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [2., 1.0, 1.0, float("inf"), 5.0, 6.0, 7.0],
            [3., 2.0, 2.0, 5.0, float("inf"), 8.0, 9.0],
            [4., 3.0, 3.0, 6.0, 8.0, float("inf"), 1.0],
            [5., 4.0, 4.0, 7.0, 9.0, 1.0, float("inf")]
        ]

        for master_row, converted_row in zip(master1, converted_matrix):
            for master_val, converted_val in zip(master_row, converted_row):
                self.assertEqual(master_val, converted_val)

        master2 = [
            [float("inf"), 1., 1., 1., 2., 3., 4., 5.],
            [1., float("inf"), float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [1., float("inf"), float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [1., float("inf"), float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [2., 1.0, 1.0, 1.0, float("inf"), 5.0, 6.0, 7.0],
            [3., 2.0, 2.0, 2.0, 5.0, float("inf"), 8.0, 9.0],
            [4., 3.0, 3.0, 3.0, 6.0, 8.0, float("inf"), 1.0],
            [5., 4.0, 4.0, 4.0, 7.0, 9.0, 1.0, float("inf")]
        ]
        converted_matrix2 = bnb.BnBPartialSolution.convert(entry_matrix, fleet_size=3)
        for master_row, converted_row in zip(master2, converted_matrix2):
            for master_val, converted_val in zip(master_row, converted_row):
                self.assertEqual(master_val, converted_val)

    def test_constructors1(self):
        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance2 = bnb.BnBPartialSolution.init_from_partial(bnbinstance)
        self.assertEqual(bnbinstance.edges, {True: [], False: []})
        self.assertEqual(bnbinstance2.edges, {True: [], False: []})

    def tests_constructors2(self):
        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.lower_bound = 30
        bnbinstance2 = bnb.BnBPartialSolution.init_from_partial(bnbinstance)
        self.assertEqual(bnbinstance2.lower_bound, 30)

        bnbinstance2.lower_bound = 35
        self.assertEqual(bnbinstance2.lower_bound, 35)

        bnbinstance3 = bnb.BnBPartialSolution.init_from_partial(bnbinstance2)
        self.assertEqual(bnbinstance3.lower_bound, 35)

        bnbinstance3.lower_bound = 15
        self.assertEqual(bnbinstance3.lower_bound, 15)

        bnbinstance2.lower_bound = 35
        self.assertEqual(bnbinstance2.lower_bound, 35)

        bnbinstance2.edges[True].append('1-2')
        self.assertEqual(bnbinstance.edges, {True: [], False: []})
        self.assertEqual(bnbinstance2.edges, {True: ['1-2'], False: []})

        self.assertEqual(len(bnbinstance.distance_matrix[0]), 10)
        self.assertEqual(len(bnbinstance.distance_matrix), 10)

    def tests_constructors3(self):
        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.lower_bound = 30

        bnbinstance2 = bnb.BnBPartialSolution.init_from_partial(bnbinstance)
        self.assertEqual(bnbinstance2.lower_bound, 30)

        bnbinstance3 = bnb.BnBPartialSolution.init_from_partial(bnbinstance)
        self.assertEqual(bnbinstance3.lower_bound, 30)

        bnbinstance3.lower_bound = 50
        bnbinstance3.leaf = True
        self.assertEqual(bnbinstance3.lower_bound, 50)
        self.assertEqual(bnbinstance2.lower_bound, 30)
        self.assertEqual(bnbinstance2.leaf, False)

        self.assertEqual(bnbinstance.lower_bound, 30)

    def tests_bound(self):
        self.instance.fleet.fleet.pop()
        self.instance.fleet.fleet.pop()
        self.instance.distance_matrix = [
            [0, 7, 1, 3, 2],
            [8, 0, 5, 3, 7],
            [1, 2, 0, 9, 4],
            [3, 1, 9, 0, 5],
            [4, 6, 7, 3, 0]
        ]
        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        LB = bnbinstance.bound()
        self.assertEqual(LB, 11.0)

    def tests_select_edge(self):
        self.instance.fleet.fleet.pop()
        self.instance.fleet.fleet.pop()
        self.instance.distance_matrix = [
            [0, 7, 1, 3, 2],
            [8, 0, 5, 3, 7],
            [1, 2, 0, 9, 4],
            [3, 1, 9, 0, 5],
            [4, 6, 7, 3, 0]
        ]
        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        LB = bnbinstance.bound()
        selected_edge = bnbinstance.select_edge()
        self.assertEqual((4, 2), selected_edge)

    def tests_construct_route(self):
        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.edges = {True: [(1, 2), (3, 5), (2, 1), (5, 4)], False: []}
        bnbinstance.construct_routes()
        self.assertEqual(bnbinstance.routes, [[(3, 5), (5, 4)], [(1, 2), (2, 1)]])
        bnbinstance.edges = {True: [(3, 5), (1, 2), (2, 1), (5, 4)], False: []}
        bnbinstance.construct_routes()
        self.assertEqual(bnbinstance.routes, [[(3, 5), (5, 4)], [(1, 2), (2, 1)]])
        bnbinstance.edges = {True: [(2, 1), (3, 5), (1, 2), (5, 4)], False: []}
        bnbinstance.construct_routes()
        self.assertEqual(bnbinstance.routes, [[(3, 5), (5, 4)], [(1, 2), (2, 1)]])

        bnbinstance.edges = {True: [(1, 2), (2, 3), (3, 5)], False: []}
        bnbinstance.construct_routes()
        self.assertEqual(bnbinstance.routes, [[(1, 2), (2, 3), (3, 5)]])
        bnbinstance.edges = {True: [(2, 3), (3, 5), (1, 2)], False: []}
        bnbinstance.construct_routes()
        self.assertEqual(bnbinstance.routes, [[(1, 2), (2, 3), (3, 5)]])

        bnbinstance.edges = {True: [(1, 3), (2, 5), (1, 4), (5, 1), (6, 1)], False: []}
        bnbinstance.construct_routes()
        self.assertEqual(bnbinstance.routes, [[(6, 1)], [(2, 5), (5, 1)], [(1, 4)], [(1, 3)]])

    def tests_routes_edges_to_nodes(self):
        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.routes = [[(3, 5), (5, 4)], [(1, 2), (2, 1)]]
        converted = bnbinstance.routes_edges_to_nodes()
        self.assertEqual(converted, [[3, 5, 4], [1, 2, 1]])

        bnbinstance.routes = [[(6, 1)], [(2, 5), (5, 1)], [(1, 4)], [(1, 3)]]
        converted = bnbinstance.routes_edges_to_nodes()
        self.assertEqual(converted, [[6, 1], [2, 5, 1], [1, 4], [1, 3]])

        bnbinstance.routes = [[(1, 2), (2, 3), (3, 5)]]
        converted = bnbinstance.routes_edges_to_nodes()
        self.assertEqual(converted, [[1, 2, 3, 5]])

    def tests_set_if_solvable(self):
        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.routes = [[(3, 5), (5, 4)], [(1, 2), (2, 1)]]
        bnbinstance.set_is_feasible()
        self.assertEqual(False, bnbinstance.is_feasible)

        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.routes = [[(3, 5)], [(1, 2), (2, 1)]]
        bnbinstance.set_is_feasible()
        self.assertEqual(True, bnbinstance.is_feasible)

        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.routes = [[(3, 5), (5, 1)], [(1, 2), (2, 1)]]
        bnbinstance.set_is_feasible()
        self.assertEqual(True, bnbinstance.is_feasible)

        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.routes = [[(3, 5), (5, 1)], [(1, 2), (2, 4), (4, 6)]]
        bnbinstance.set_is_feasible()
        self.assertEqual(False, bnbinstance.is_feasible)

        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.routes = [[(1, 3), (3, 1)], [(1, 2), (2, 5), (5, 2)]]
        bnbinstance.set_is_feasible()
        self.assertEqual(True, bnbinstance.is_feasible)

    def tests_is_and_solve_leaf(self):

        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        self.assertFalse(bnbinstance.is_leaf())

        bnbinstance.distance_matrix = numpy.array([[1, 0], [1, 2]])
        with self.assertRaises(ValueError):
            bnbinstance.is_leaf()

        bnbinstance.distance_matrix = numpy.array([[float("inf"), 0, 1],
                                                  [1, 2, float("inf")],
                                                  [2, float("inf"), 0]])
        self.assertTrue(bnbinstance.is_leaf())
        bnbinstance.solve_leaf_first()
        self.assertEqual(bnbinstance.edges[True], [(1, 0), (2, 1)])

        bnbinstance.distance_matrix = numpy.array([[float("inf"), 0, 3],
                                                  [1, float("inf"), 2],
                                                  [2, 0, float("inf")]])
        bnbinstance.edges = {True: [], False: []}
        self.assertTrue(bnbinstance.is_leaf())
        bnbinstance.solve_leaf_second()
        self.assertEqual(bnbinstance.edges[True], [(1, 3), (2, 0)])

        bnbinstance.distance_matrix = numpy.array([[float("inf"), 0, 3],
                                                  [1, float("inf"), float("inf")],
                                                  [2, 0, float("inf")]])
        bnbinstance.edges = {True: [], False: []}
        self.assertTrue(bnbinstance.is_leaf())
        with self.assertRaises(ValueError):
            bnbinstance.solve_leaf_first()


class TestBnBPartialSolution_2(unittest.TestCase):

    def setUp(self):
        raw_data = dm.Importer()
        raw_data.import_data("./tests/cvrp2.test")
        data = dm.DataMapper(raw_data)

        self.instance = i.ProblemInstance(data)

        self.instance.distance_matrix = [
            [0, 6, 3, 1, 7, 11],
            [6, 0, 5, 9, 6, 3],
            [3, 5, 0, 8, 2, 4],
            [1, 9, 8, 0, 9, 9],
            [7, 6, 2, 9, 0, 3],
            [11,3, 4, 9, 3, 0]
        ]

        self.bounded_master = [
            [float("inf"), 1., 1., 2., 3., 4., 5., 6.],
            [1., float("inf"), float("inf"), 5., 2., 0., 6., 10.],
            [1., float("inf"), float("inf"), 5., 2., 0., 6., 10.],
            [2., 3., 3., float("inf"), 2., 6., 3., 0.],
            [3., 1., 1., 3., float("inf"), 6., 3., 0., 2.],
            [4., 0., 0., 8., 7., float("inf"), 8., 8.],
            [5., 5., 5., 4., 0., 7., float("inf"), 1.],
            [6., 8., 8., 0., 1., 6., 0., float("inf")]
        ]

    def tests_edge_to_real_indexes(self):
        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.bound()
        real = bnbinstance.edge_to_real_indexes((2, 3))
        self.assertEqual([(3, 4)], real)

        real = bnbinstance.edge_to_real_indexes((3, 5))
        self.assertEqual([(4, 6)], real)

        real = bnbinstance.edge_to_real_indexes((1, 4))
        self.assertEqual([(1, 5), (2, 5)], real)

        real = bnbinstance.edge_to_real_indexes((3, 1))
        self.assertEqual([(4, 1), (4, 2)], real)

        # after row-column deletion:
        bnbinstance.with_edge_branch((2, 6))

        real = bnbinstance.edge_to_real_indexes((3, 5))
        self.assertEqual([(3, 6)], real)

        real = bnbinstance.edge_to_real_indexes((1, 4))
        self.assertEqual([(1, 5), (2, 5)], real)

        real = bnbinstance.edge_to_real_indexes((2, 3))
        self.assertEqual([], real)

        real = bnbinstance.edge_to_real_indexes((3, 6))
        self.assertEqual([], real)

        # after another row-column deletion:
        bnbinstance.with_edge_branch((1, 4))

        real = bnbinstance.edge_to_real_indexes((3, 5))
        self.assertEqual([(2, 5)], real)

        real = bnbinstance.edge_to_real_indexes((1, 3))
        self.assertEqual([(1, 4)], real)

        real = bnbinstance.edge_to_real_indexes((3, 1))
        self.assertEqual([(2, 1), (2, 2)], real)

        real = bnbinstance.edge_to_real_indexes((1, 4))
        self.assertEqual([], real)

        real = bnbinstance.edge_to_real_indexes((2, 3))
        self.assertEqual([], real)

        real = bnbinstance.edge_to_real_indexes((3, 6))
        self.assertEqual([], real)

    def tests_with_edge_branch(self):
        master = numpy.array([
                    [float("inf"), 1., 1., 2., 3., 4., 6.],
                    [1., float("inf"), float("inf"), 5., 1., 0., 10.],
                    [1., float("inf"), float("inf"), 5., 1., 0., 10.],
                    [2., 3., 3., float("inf"), 1., 6., 0.],
                    [4., 0., 0., 8., 6., float("inf"), 8.],
                    [5., 4., 4., 3., float("inf"), 6., 0.],
                    [6., 8., 8., 0., 0., 6., float("inf")]
                ])
        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.bound()
        self.assertEqual(bnbinstance.lower_bound, 13.0)
        bnbinstance.with_edge_branch((3, 5))
        self.assertEqual(bnbinstance.edges, {True: [(3, 5)], False: [(5, 3)]})
        for row, row_master in zip(master, bnbinstance.distance_matrix):
            for val, val_master in zip(row, row_master):
                self.assertEqual(val, val_master)
        self.assertEqual(bnbinstance.lower_bound, 15.0)

    def tests_without_edge_branch(self):
        master = [
            [float("inf"), 1., 1., 2., 3., 4., 5., 6.],
            [1., float("inf"), float("inf"), 5., 2., 0., 6., 10.],
            [1., float("inf"), float("inf"), 5., 2., 0., 6., 10.],
            [2., 3., 3., float("inf"), 2., 6., 3., 0.],
            [3., 0., 0., 2., float("inf"), 5., float("inf"), 1.],
            [4., 0., 0., 8., 7., float("inf"), 8., 8.],
            [5., 5., 5., 4., 0., 7., float("inf"), 1.],
            [6., 8., 8., 0., 1., 6., 0., float("inf")]
        ]
        master = numpy.array(master)

        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.bound()
        self.assertEqual(bnbinstance.lower_bound, 13.0)

        bnbinstance.without_edge_branch((3, 5))

        self.assertEqual(bnbinstance.edges, {True: [], False: [(3, 5)]})
        for row, row_master in zip(master, bnbinstance.distance_matrix):
            for val, val_master in zip(row, row_master):
                self.assertEqual(val, val_master)

        self.assertEqual(bnbinstance.lower_bound, 14.0)


if __name__ == "__main__":
    unittest.main()
