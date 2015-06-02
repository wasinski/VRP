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
        converted_matrix = bnb.convert(entry_matrix, fleet_size=2)
        master = [
            [float("inf"), 1, 1, 2, 3, 4, 5],
            [1, float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [1, float("inf"), float("inf"), 1.0, 2.0, 3.0, 4.0],
            [2, 1.0, 1.0, float("inf"), 5.0, 6.0, 7.0],
            [3, 2.0, 2.0, 5.0, float("inf"), 8.0, 9.0],
            [4, 3.0, 3.0, 6.0, 8.0, float("inf"), 1.0],
            [5, 4.0, 4.0, 7.0, 9.0, 1.0, float("inf")]
        ]

        self.assertEqual(master, converted_matrix)


if __name__ == "__main__":
    unittest.main()
