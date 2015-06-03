import unittest
from code import branchnbound as bnb


class TestBnB(unittest.TestCase):
    pass


class TestBnBPartialSolution(unittest.TestCase):

    def setUp(self):
        pass

    def test_convert(self):
        entry_matrix = [
            [0, 1, 2, 3, 4],
            [1, 0, 5, 6, 7],
            [2, 5, 0, 8, 9],
            [3, 6, 8, 0, 1],
            [4, 7, 9, 1, 0]
        ]
        converted_matrix = bnb.BnBPartialSolution.convert(entry_matrix, fleet_size=2)
        master1 = [
            [float("inf"), 1., 1., 2., 3., 4., 5.],
            [1., float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [1., float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [2., 1.0, 1.0, float("inf"), 5.0, 6.0, 7.0],
            [3., 2.0, 2.0, 5.0, float("inf"), 8.0, 9.0],
            [4., 3.0, 3.0, 6.0, 8.0, float("inf"), 1.0],
            [5., 4.0, 4.0, 7.0, 9.0, 1.0, float("inf")]
        ]

        for master_row, converted_row in zip(master1, converted_matrix):
            for master_val, converted_val in zip(master_row, converted_row):
                self.assertEqual(master_val, converted_val)

        master2 = [
            [float("inf"), 1., 1., 1., 2., 3., 4., 5.],
            [1., float("inf"), float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [1., float("inf"), float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [1., float("inf"), float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [2., 1.0, 1.0, 1.0, float("inf"), 5.0, 6.0, 7.0],
            [3., 2.0, 2.0, 2.0, 5.0, float("inf"), 8.0, 9.0],
            [4., 3.0, 3.0, 3.0, 6.0, 8.0, float("inf"), 1.0],
            [5., 4.0, 4.0, 4.0, 7.0, 9.0, 1.0, float("inf")]
        ]
        converted_matrix2 = bnb.BnBPartialSolution.convert(entry_matrix, fleet_size=3)
        for master_row, converted_row in zip(master2, converted_matrix2):
            for master_val, converted_val in zip(master_row, converted_row):
                self.assertEqual(master_val, converted_val)

if __name__ == "__main__":
    unittest.main()
