import unittest
from code import baseobjects as bo


class TestNode(unittest.TestCase):

    def setUp(self):
        self.node0 = bo.Node(0, (33, 66), 100)
        self.node1 = bo.Node(1, (33, 66), 100)
        self.node2 = bo.Node(2, (99, 77), 200)

    def test_init(self):
        self.node0 = bo.Node(0, (33, 66), 100)
        self.assertEqual(self.node0.id, 0)
        self.assertEqual(self.node0.coordinates, (33, 66))
        self.assertEqual(self.node0.demand, 100)

    def test_equal(self):
        self.assertTrue(self.node0 == self.node1)
        self.assertFalse(self.node0 == self.node2)
        with self.assertRaises(TypeError):
            self.node0 == 1


class TestVehicle(unittest.TestCase):

    def setUp(self):
        self.vehicle0 = bo.Vehicle(1000)
        self.vehicle1 = bo.Vehicle(2000)

    def test_init(self):
        self.assertEqual(self.vehicle0.id, 0)
        self.assertEqual(self.vehicle0.capacity, 1000)
        self.assertEqual(self.vehicle0.route, [])
        self.assertEqual(self.vehicle1.id, 1)
        self.assertEqual(self.vehicle1.capacity, 2000)

    def test_load(self):
        self.vehicle0.set_load(500)
        self.assertEqual(self.vehicle0.get_load(), 500)
        self.vehicle0.add_load(200)
        self.assertEqual(self.vehicle0.get_load(), 700)
        self.vehicle0.subtract_load(200)
        self.assertEqual(self.vehicle0.get_load(), 500)
        with self.assertRaises(ValueError):
            self.vehicle0.add_load(501)
        with self.assertRaises(ValueError):
            self.vehicle0.subtract_load(501)


class TestRoute(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        pass


class TestNetwork(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        pass

if __name__ == "__main__":
    unittest.main()
