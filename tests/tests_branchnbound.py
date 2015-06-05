import unittest
import numpy
from code import branchnbound as bnb
from code import instance as i
from code import datamapping as dm


class TestBnB(unittest.TestCase):

    def setUp(self):
        raw_data = dm.Importer()
        raw_data.import_data("./tests/cvrp1.test")
        data = dm.DataMapper(raw_data)

        self.instance = i.ProblemInstance(data)

    def test_initialize(self):
        pass

    def test_run(self):
        pass

    def test_pop_most_promising(self):
        pass


class TestBnBPartialSolution(unittest.TestCase):

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
        bnbinstance3.solvable = False
        self.assertEqual(bnbinstance3.lower_bound, 50)
        self.assertEqual(bnbinstance2.lower_bound, 30)
        self.assertEqual(bnbinstance2.solvable, True)

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
        bnbinstance.set_is_solvable()
        self.assertEqual(False, bnbinstance.solvable)

        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.routes = [[(3, 5)], [(1, 2), (2, 1)]]
        bnbinstance.set_is_solvable()
        self.assertEqual(True, bnbinstance.solvable)

        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.routes = [[(3, 5), (5, 1)], [(1, 2), (2, 1)]]
        bnbinstance.set_is_solvable()
        self.assertEqual(True, bnbinstance.solvable)

        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.routes = [[(3, 5), (5, 1)], [(1, 2), (2, 4), (4, 6)]]
        bnbinstance.set_is_solvable()
        self.assertEqual(False, bnbinstance.solvable)

        bnbinstance = bnb.BnBPartialSolution.init_from_instance(self.instance)
        bnbinstance.routes = [[(1, 3), (3, 1)], [(1, 2), (2, 5), (5, 2)]]
        bnbinstance.set_is_solvable()
        self.assertEqual(True, bnbinstance.solvable)

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
        bnbinstance.solve_leaf()
        self.assertEqual(bnbinstance.edges[True], [(1, 0), (2, 1)])

        bnbinstance.distance_matrix = numpy.array([[float("inf"), 0, 3],
                                                  [1, float("inf"), 2],
                                                  [2, 0, float("inf")]])
        bnbinstance.edges = {True: [], False: []}
        self.assertTrue(bnbinstance.is_leaf())
        bnbinstance.solve_leaf()
        self.assertEqual(bnbinstance.edges[True], [(1, 3), (2, 0)])

        bnbinstance.distance_matrix = numpy.array([[float("inf"), 0, 3],
                                                  [1, float("inf"), float("inf")],
                                                  [2, 0, float("inf")]])
        bnbinstance.edges = {True: [], False: []}
        self.assertTrue(bnbinstance.is_leaf())
        with self.assertRaises(ValueError):
            bnbinstance.solve_leaf()


if __name__ == "__main__":
    unittest.main()
