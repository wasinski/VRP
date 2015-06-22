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

    def test_deep_copy(self):

        self.assertEqual(self.tabu_search.instance.solution.fleet[0].route[0].id, self.tabu_search.best_instance.solution.fleet[0].route[0].id)
        self.tabu_search.instance.solution.fleet[0].route[0].id = 666
        self.assertNotEqual(self.tabu_search.instance.solution.fleet[0].route[0].id, self.tabu_search.best_instance.solution.fleet[0].route[0].id)

    def test_get_sorted_edges(self):
        edges = self.tabu_search.get_sorted_edges(self.tabu_search.instance.solution.fleet[0])
        self.assertTrue(self.tabu_search.instance.distance_between(edges[0][0], edges[0][1]) <
                        self.tabu_search.instance.distance_between(edges[-1][0], edges[-1][1]))

    def test_best_neighbours(self):
        neighbours = self.tabu_search.best_neighbours(2)
        self.assertTrue(neighbours[0][1]>neighbours[-1][1])
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
        greedy.run(sort=False)
        self.solution.value = self.solution.eval()
        self.tabu_search = tabu.TabuSearch(self.solution, 100)

    # def test_general(self):
    #     print("value before: " + str(self.tabu_search.best_instance.eval()))
    #     self.tabu_search.run()
    #     print("value after: " + str(self.tabu_search.best_instance.eval()))


if __name__ == "__main__":
    unittest.main()
