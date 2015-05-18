import unittest
from code import datamapping as dm


class TestDataMapper(unittest.TestCase):

    def setUp(self):
        test_object = dm.Importer()
        test_object.import_data("./tests/cvrp1.test")

    def test_blablabla(self):
        pass

if __name__ == "__main__":
    unittest.main()
