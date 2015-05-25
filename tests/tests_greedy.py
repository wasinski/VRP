import unittest
from code import greedyfirst as gf
from code import algorithm as a
from code import instance as i
from code import datamapping as dm


class TestGreedy(unittest.TestCase):

    def setUp(self):
        raw_data = dm.Importer()
        raw_data.import_data("./tests/cvrp1.test")
        data = dm.DataMapper(raw_data)

        problem = i.ProblemInstance(data)
        self.solution = a.Solution(problem)

    def test_greedy(self):
        self.solution = gf.GreedyFirst.run(self.solution)  # trzeba będzie zmienić na "zwracanie" best solution i przyjmowaniu current solution
        # tzn przed przypisaniem do best należy wykonać test czy rzeczywiście jest best ;)
        # tak właśnie powinna wyglądać iteracja!

if __name__ == "__main__":
    unittest.main()
