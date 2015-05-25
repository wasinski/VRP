import unittest
from code import greedyfirst as gf
from code import algorithm as a
from code import instance as i
from code import datamapping as dm


class TestGreedy(unittest.TestCase):

    def setUp(self):
        raw_data = dm.Importer()
        raw_data.import_data("./tests/E-n23-k3.vrp")
        data = dm.DataMapper(raw_data)

        problem = i.ProblemInstance(data)
        self.solution = a.Solution(problem)

    def test_greedy(self):

        self.solution.best_solution = gf.GreedyFirst.run(self.solution.current_solution)
        count = 0
        for vehicle in self.solution.best_solution.fleet.fleet:
            for node in vehicle.route:
                count += 1
        self.assertEqual(count, 28)  # 28 because every vehicle stats and ends at the depot
        self.assertEqual(self.solution.best_solution.fleet.fleet[0].load, 4450)
        self.assertEqual(self.solution.best_solution.fleet.fleet[1].load, 4475)
        self.assertEqual(self.solution.best_solution.fleet.fleet[2].load, 1264)

if __name__ == "__main__":
    unittest.main()
