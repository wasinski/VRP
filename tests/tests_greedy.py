import unittest
from code import greedyfirst as gf
from code import algorithm as a
from code import instance as i
from code import datamapping as dm
from code import baseobjects as bo


class TestGreedy(unittest.TestCase):

    def setUp(self):
        raw_data = dm.Importer()
        raw_data.import_data("./tests/E-n23-k3.vrp")
        data = dm.DataMapper(raw_data)

        problem = i.ProblemInstance(data)
        self.solution = a.Solution(problem)

    def test_get_nearest_node(self):
        greedy = gf.GreedyFirst(self.solution.current_solution)
        node1 = bo.Node(1, (2, 2), 50)
        node2 = bo.Node(2, (3, 3), 60)
        node3 = bo.Node(3, (4, 4), 70)
        node4 = bo.Node(4, (5, 5), 80)
        greedy.distance_matrix = [
            [0, 4, 3, 1],
            [2, 0, 4, 1],
            [5, 2, 0, 3],
            [2, 1, 7, 0]
        ]
        nearest = greedy.get_nearest_node(1, [node4, node2])
        self.assertEqual(nearest, 4)

        nearest = greedy.get_nearest_node(2, [node3, node1])
        self.assertEqual(nearest, 1)

        nearest = greedy.get_nearest_node(3, [node1, node2])
        self.assertEqual(nearest, 2)

        nearest = greedy.get_nearest_node(4, [node1, node2, node3])
        self.assertEqual(nearest, 2)

    def test_greedy_sort_false(self):
        greedy = gf.GreedyFirst(self.solution.current_solution)
        self.solution.best_solution = greedy.run(sort=False)
        count = 0
        for vehicle in self.solution.best_solution.fleet.fleet:
            for node in vehicle.route:
                count += 1
        self.assertEqual(count, 28)  # 28 because every vehicle stats and ends at the depot
        self.assertEqual(self.solution.best_solution.fleet[0].load, 4450)
        self.assertEqual(self.solution.best_solution.fleet[1].load, 4475)
        self.assertEqual(self.solution.best_solution.fleet[2].load, 1264)
        for vehicle in self.solution.best_solution.fleet.fleet:
            for node in vehicle.route.route:
                print (node.id)
        print("-------------")

    def test_greedy_sort_true(self):
        greedy = gf.GreedyFirst(self.solution.current_solution)
        self.solution.best_solution = greedy.run(sort=False)
        count = 0
        for vehicle in self.solution.best_solution.fleet.fleet:
            for node in vehicle.route:
                count += 1
        self.assertEqual(count, 28)  # 28 because every vehicle stats and ends at the depot
        self.assertEqual(self.solution.best_solution.fleet[0].load, 4450)
        self.assertEqual(self.solution.best_solution.fleet[1].load, 4475)
        self.assertEqual(self.solution.best_solution.fleet[2].load, 1264)
        for vehicle in self.solution.best_solution.fleet.fleet:
            for node in vehicle.route.route:
                print (node.id)

if __name__ == "__main__":
    unittest.main()
