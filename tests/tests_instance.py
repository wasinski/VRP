import unittest
from code import instance as i
from code import datamapping as dm


class TestProblemInstance(unittest.TestCase):

    def setUp(self):
        raw_data = dm.Importer()
        raw_data.import_data("./tests/cvrp1.test")
        data = dm.DataMapper(raw_data)

        self.problem = i.ProblemInstance(data)

    def test_(self):
        pass


if __name__ == "__main__":
    unittest.main()
