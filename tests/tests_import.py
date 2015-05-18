import unittest
from code import datamapping as dm


class TestsImporter(unittest.TestCase):

    def setUp(self):
        self.test_filelines = [
            "NAME : test-E-n6-k4",
            "COMMENT : (##This is bullshit##Christophides and Eilon, Min no of trucks: 4, Optimal value: 375)",
            "TYPE : CVRP",
            "DIMENSION : 6",
            "EDGE_WEIGHT_TYPE : EUC_2D",
            "CAPACITY : 2000",
            "NODE_COORD_SECTION",
            "1 145 215",
            "2 151 264",
            "3 159 261",
            "4 130 254",
            "5 128 252",
            "6 163 247",
            "DEMAND_SECTION",
            "1 0",
            "2 1100",
            "3 700",
            "4 800",
            "5 1400",
            "6 2100",
            "DEPOT_SECTION",
            " 1",
            " -1",
            "EOF"
        ]

        self.test_node_coordinates_list = [
            (float(145), float(215)),
            (float(151), float(264)),
            (float(159), float(261)),
            (float(130), float(254)),
            (float(128), float(252)),
            (float(163), float(247))
        ]

        self.test_demand_list = [0, 1100, 700, 800, 1400, 2100]

        self.testobject = dm.Importer()
        self.testobject._read_file("./tests/cvrp1.test")

    def test_read_file(self):
        self.testobject._read_file("./tests/cvrp1.test")
        reference = self.test_filelines
        self.assertEqual(len(self.testobject.file_lines), len(reference))
        for line, ref in zip(self.testobject.file_lines, reference):
            self.assertEqual(line, ref)

    def test_read_info(self):
        self.testobject.import_data("./tests/cvrp1.test")

        info, breaklines = self.testobject._read_info()
        self.assertEqual(breaklines[0], 6)
        self.assertEqual(breaklines[1], 13)
        self.assertEqual(breaklines[2], 20)

        self.assertEqual(info["NAME"], "test-E-n6-k4")
        self.assertEqual(info["DIMENSION"], "6")

    def test_return_nodes_and_delivery_lists(self):
        self.testobject.import_data("./tests/cvrp1.test")
        node_coordinates_list, demand_list = self.testobject._return_nodes_and_delivery_lists((6, 13, 20))

        ref_node_coord = self.test_node_coordinates_list
        ref_demand_list = self.test_demand_list

        self.assertEqual(node_coordinates_list, ref_node_coord)
        self.assertEqual(demand_list, ref_demand_list)

    def test_create_adjacency_matrix(self):
        self.testobject.import_data("./tests/cvrp1.test")
        matrix = self.testobject._create_distance_matrix(self.test_node_coordinates_list, 6)
        for i, row in enumerate(matrix):
            matrix[i] = list(map(int, row))

        refmatrix = [
            [0, 49, 48, 41, 40, 36],
            [49, 0, 8, 23, 25, 20],
            [48, 8, 0, 29, 32, 14],
            [41, 23, 29, 0, 2, 33],
            [40, 25, 32, 2, 0, 35],
            [36, 20, 14, 33, 35, 0]
        ]
        self.assertEqual(matrix, refmatrix)

    def test_import(self):
        self.testobject.import_data("./tests/cvrp1.test")
        self.assertEqual(self.testobject.distance_matrix[0][0], 0)
        self.assertEqual(self.testobject.distance_matrix[5][5], 0)
        self.assertEqual(self.testobject.demand_array[0], 0)
        self.assertEqual(self.testobject.demand_array[5], 2100)


if __name__ == '__main__':
    unittest.main()
