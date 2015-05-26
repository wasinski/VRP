import unittest
from code import baseobjects as bo


class TestNode(unittest.TestCase):

    def setUp(self):
        self.node0 = bo.Node(0, (33, 66), 100)
        self.node1 = bo.Node(0, (33, 66), 100)
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


class TestRoute(unittest.TestCase):

    def setUp(self):
        self.node0 = bo.Node(0, (9, 66), 0)
        self.node1 = bo.Node(1, (33, 66), 100)
        self.node2 = bo.Node(2, (99, 77), 200)

    def test_init(self):
        route1 = bo.Route()
        route1.append_node(self.node0)
        with self.assertRaises(ValueError):
            route1.append_node(self.node0)

        route1.append_node(self.node1)
        self.assertEqual(route1.get_route(), [self.node0, self.node1])

        route1.insert_node(1, self.node2)
        self.assertEqual(route1.get_route(), [self.node0, self.node2, self.node1])

        with self.assertRaises(ValueError):
            route1.insert_node(1, self.node0)

        route1.switch_nodes_internaly(1, 2)
        self.assertEqual(route1.get_route(), [self.node0, self.node1, self.node2])


class TestVehicle(unittest.TestCase):

    def setUp(self):
        self.vehicle0 = bo.Vehicle(1000)
        self.vehicle1 = bo.Vehicle(2000)

    def test_init(self):
        self.assertEqual(self.vehicle0.capacity, 1000)
        self.assertEqual(self.vehicle0.route.route, bo.Route().route)
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


class TestNetwork(unittest.TestCase):

    def setUp(self):
        self.node0 = bo.Node(0, (9, 66), 0)
        self.node1 = bo.Node(1, (33, 66), 100)
        self.node2 = bo.Node(2, (99, 77), 200)

    def test_init_and_append(self):
        network = bo.Network()
        network.append_node(self.node0)
        network.append_node(self.node1)
        self.assertEqual(network.network, [self.node0, self.node1])

    def test_iter(self):
        network = bo.Network()
        network.append_node(self.node0)
        network.append_node(self.node2)
        network.append_node(self.node1)
        master = [self.node0, self.node2, self.node1]
        for master_node, node in zip(master, network):
            self.assertEqual(master_node, node)

    def test_sort_network_by_demand(self):
        network = bo.Network()
        network.append_node(self.node0)
        network.append_node(self.node2)
        network.append_node(self.node1)
        network.sort_network_by_demand()
        master = [self.node2, self.node1, self.node0]
        for master_node, node in zip(master, network):
            self.assertEqual(master_node, node)


class TestFleet(unittest.TestCase):

    def setUp(self):
        self.vehicle0 = bo.Vehicle(1000)
        self.vehicle1 = bo.Vehicle(2000)

    def test_init_and_append(self):
        fleet = bo.Fleet()
        fleet.append_vehicle(self.vehicle0)
        fleet.append_vehicle(self.vehicle1)
        self.assertEqual(fleet.fleet, [self.vehicle0, self.vehicle1])

    def test_iter(self):
        fleet = bo.Fleet()
        fleet.append_vehicle(self.vehicle0)
        fleet.append_vehicle(self.vehicle1)
        master = [self.vehicle0, self.vehicle1]
        for master_vehicle, vehicle in zip(master, fleet):
            self.assertEqual(master_vehicle, vehicle)


if __name__ == "__main__":
    unittest.main()
