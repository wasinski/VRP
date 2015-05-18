import unittest
from code import datamapping as dm


class TestDataMapper(unittest.TestCase):

    def setUp(self):
        self.test_object = dm.Importer()
        self.test_object.import_data("./tests/cvrp1.test")

    def test_init(self):
        data_mapper = dm.DataMapper(self.test_object)
        print (data_mapper)

if __name__ == "__main__":
    unittest.main()
