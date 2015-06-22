import unittest

from code import instance as i
from code import datamapping as dm
from code import greedyfirst as gf
from code import algorithm as a
from code import baseobjects as bo

from code import tabu


class TestTabuSpecific(unittest.TestCase):

    def setUp(self):
        raw_data = dm.Importer()
        # raw_data.import_data("./tests/cvrp2.test")
        # raw_data.import_data("./tests/ulysses-n16-k3.vrp")
        raw_data.import_data("./tests/E-n23-k3.vrp")
        # raw_data.import_data("./tests/cvrp3.test")
        # raw_data.import_data("./tests/P-n19-k2.vrp")
        data = dm.DataMapper(raw_data)
        self.instance = i.ProblemInstance(data)
        self.solution = a.Solution(self.instance)

        greedy = gf.GreedyFirst(self.solution.solution)
        greedy.run(sort=False)
        self.solution.value = self.solution.eval()
        self.tabu_search = tabu.TabuSearch(self.solution, 100)

    def test_swap_2opt(self):

        node1 = bo.Node(1, (1, 1), 100)
        node2 = bo.Node(2, (1, 1), 100)
        node3 = bo.Node(3, (1, 1), 100)
        node4 = bo.Node(4, (1, 1), 100)
        node5 = bo.Node(5, (1, 1), 100)

        route = bo.Route()
        route.set_route([node1, node2, node3, node4, node5])

        new_route = self.tabu_search.swap_2opt(route, 2, 4)
        self.assertEqual(len([1, 4, 3, 2, 5]), len(new_route))
        for node, id_ in zip(new_route, [1, 4, 3, 2, 5]):
            self.assertEqual(node.id, id_)

    def test_swap_intra(self):

        node1 = bo.Node(1, (1, 1), 100)
        node2 = bo.Node(2, (1, 1), 100)
        node3 = bo.Node(3, (1, 1), 100)
        node4 = bo.Node(4, (1, 1), 100)
        node5 = bo.Node(5, (1, 1), 100)

        node6 = bo.Node(6, (1, 1), 100)
        node7 = bo.Node(7, (1, 1), 100)

        src_route = bo.Route()
        dest_route = bo.Route()

        src_route.set_route([node1, node2, node3, node4, node5, node1])
        dest_route.set_route([node1, node6, node7, node1])
        new_dest_route = self.tabu_search.swap_intra(src_route, dest_route, 4)

        self.assertEqual(len(new_dest_route), 5)
        self.assertEqual(len(src_route), 5)
        ids = [1, 6, 7, 4, 1]
        for node, id_ in zip(new_dest_route, ids):
            self.assertEqual(id_, node.id)

        with self.assertRaises(ValueError):
            new_dest_route = self.tabu_search.swap_intra(src_route, dest_route, 1)

    def test_deep_copy(self):

        self.assertEqual(self.tabu_search.instance.solution.fleet[0].route[0].id, self.tabu_search.best_instance.solution.fleet[0].route[0].id)
        self.tabu_search.instance.solution.fleet[0].route[0].id = 666
        self.assertNotEqual(self.tabu_search.instance.solution.fleet[0].route[0].id, self.tabu_search.best_instance.solution.fleet[0].route[0].id)

    def test_choose_node(self):
        print (self.tabu_search.choose_node(self.tabu_search.instance.solution.fleet[0].route))

    # def test_optimize_internal(self):
    #     self.tabu_search.optimize_internal()


class TestTabuGeneral(unittest.TestCase):

    def setUp(self):
        raw_data = dm.Importer()
        # raw_data.import_data("./tests/cvrp2.test")
        # raw_data.import_data("./tests/ulysses-n16-k3.vrp")
        # raw_data.import_data("./tests/E-n23-k3.vrp")
        # raw_data.import_data("./tests/cvrp3.test")
        raw_data.import_data("./tests/P-n19-k2.vrp")
        data = dm.DataMapper(raw_data)
        self.instance = i.ProblemInstance(data)
        self.solution = a.Solution(self.instance)

        greedy = gf.GreedyFirst(self.solution.solution)
        greedy.run(sort=True)
        self.solution.value = self.solution.eval()
        self.tabu_search = tabu.TabuSearch(self.solution, 100)

    def test_general(self):
        print("value before: " + str(self.tabu_search.best_instance.eval()))
        self.tabu_search.run()
        print("value after: " + str(self.tabu_search.best_instance.eval()))


if __name__ == "__main__":
    unittest.main()
