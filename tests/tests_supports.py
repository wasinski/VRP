import unittest
from CVRPSolver import supports as s


class TestsImporter(unittest.TestCase):

    def setUp(self):
        self.test_filelines = [
            "NAME : E-n6-k4-test",
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

    def test_read_file(self):
        lines = s.Importer._read_file("./tests/cvrp1.test")
        reference = self.test_filelines
        self.assertEqual(len(lines), len(reference))
        for line, ref in zip(lines, reference):
            self.assertEqual(line, ref)

    def test_read_info(self):
        filelines = self.test_filelines

        info, breaklines = s.Importer._read_info(filelines)
        self.assertEqual(breaklines[0], 6)
        self.assertEqual(breaklines[1], 13)
        self.assertEqual(breaklines[2], 20)

        self.assertEqual(info["NAME"], "E-n6-k4-test")
        self.assertEqual(info["DIMENSION"], "6")

    def test_return_nodes_and_delivery_lists(self):
        filelines = self.test_filelines
        node_coordinates_list, demand_list = s.Importer._return_nodes_and_delivery_lists(filelines, (6, 13, 20))

        ref_node_coord = self.test_node_coordinates_list
        ref_demand_list = self.test_demand_list

        self.assertEqual(node_coordinates_list, ref_node_coord)
        self.assertEqual(demand_list, ref_demand_list)

    def test_create_adjacency_matrix(self):
        matrix = s.Importer._create_adjacency_matrix(self.test_node_coordinates_list, 6)
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

    def test_euclidian_distance(self):
        probe1 = s.Importer._euclidian_distance((-1, -1), (-1, 2))
        probe2 = s.Importer._euclidian_distance((123, 12), (11, 234))
        probe3 = s.Importer._euclidian_distance((11, 76), (98, 1))

        self.assertAlmostEqual(probe1, 3.0, places=2)
        self.assertAlmostEqual(probe2, 248.65, places=2)
        self.assertAlmostEqual(probe3, 114.865, places=3)

    def test_import(self):
        matrix_array, demand_array = s.Importer.import_data("./tests/cvrp1.test")
        self.assertEqual(matrix_array[0][0], 0)
        self.assertEqual(matrix_array[5][5], 0)
        self.assertEqual(demand_array[0], 0)
        self.assertEqual(demand_array[5], 2100)


if __name__ == '__main__':
    unittest.main()
