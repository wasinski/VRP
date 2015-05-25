class Node(object):

    def __init__(self, my_id, my_node_coordinates, my_demand):
        self.id = my_id
        self.coordinates = my_node_coordinates
        self.demand = my_demand
        self.visited = False

    def __eq__(self, other):
        if not isinstance(other, Node):
            print("you tried to compare different type of object (correct: Node)")
            raise TypeError
        else:
            if self.id == other.id:
                return True
            else:
                return False

    def get_id(self):
        return self.id

    def get_demand(self):
        return self.demand

    def get_coordinates(self):
        return self.coordinates

    def set_visited(self, state):
        self.visited = state


  # duże zmiany w tej klasie się szykują, bo trzeba będzie do route przypisać Route!
class Vehicle(object):

    __id = 0

    def __init__(self, my_capacity):
        self.id = Vehicle.__id
        Vehicle.__id += 1
        self.capacity = my_capacity
        self.route = []
        self.load = 0

    def set_route(self, my_route):
        self.route = my_route

    def set_route_add_node(self, my_node):
        self.route.append(my_node)

    def get_capacity(self):
        return self.capacity

    def set_load(self, load):
        self.load = load

    def add_load(self, cargo):
        if self.load + cargo <= self.capacity:
            self.load += cargo
        else:
            print("couldnt add more cargo!")
            print("vehicle id:" + str(self.id) + " load:" + str(self. load) +
                  " cargo:" + str(cargo) + " capacity:" + str(self.capacity))
            raise ValueError

    def subtract_load(self, cargo):
        if self.load - cargo >= 0:
            self.load -= cargo
        else:
            print("couldnt subtract cargo!")
            print("vehicle id:" + str(self.id) + " load:" + str(self. load) +
                  " cargo:" + str(cargo) + " capacity:" + str(self.capacity))
            raise ValueError

    def add_node(self, node):
        try:
            self.add_load(node.demand)
            self.set_route_add_node(node)
            node.visited = True
        except ValueError as e:
            raise e

    def get_load(self):
        return self.load

    def get_route(self):
        return self.route


class Network(object):

    def __init__(self, my_network=None):
        if isinstance(my_network, Network):
            self.network = my_network
        else:
            self.network = []

    def __iter__(self):
        for node in self.network:
            yield node

    def set_network(self, my_network):
        self.network = my_network

    def append_node(self, node):
        self.network.append(node)

    def sort_network_by_demand(self):  # TODO: ta funkcja jest KONIECZNIE do sprawdzenia!
        self.network.sort(cmp=lambda x, y: cmp(x.demand, y.demand, key=self.network.node))


class Fleet(object):

    def __init__(self, my_fleet=None):
        if isinstance(my_fleet, Fleet):
            self.fleet = my_fleet
        else:
            self.fleet = []

    def __iter__(self):
        for vehicle in self.fleet:
            yield vehicle

    def set_fleet(self, my_fleet):
        self.fleet = my_fleet

    def append_vehicle(self, vehicle):
        self.fleet.append(vehicle)

    def get_vehicle(self, id_):
        for vehicle in self.fleet:
            if vehicle.id == id_:
                return id_
        print("no match found for given id!")
        raise ValueError


class Route(object):

    def __init__(self):
        self.route = []

    def set_route(self, route):
        self.route = route

    def append_node(self, node):
        if node not in self.route:
            self.route.append(node)
        else:
            print("node already in the route!")
            raise ValueError

    def set_node(self, index, node):
        if not isinstance(node, Node):
            print("given argument is not a Node!")
            raise TypeError
        if node not in self.route:
            self.route[index] = node
        else:
            print("node already in the route!")
            raise ValueError

    def insert_node(self, index, node):
        if not isinstance(node, Node):
            print("given argument is not a Node!")
            raise TypeError
        if node not in self.route:
            self.route.insert(index, node)
        else:
            print("node already in the route!")
            raise ValueError

    def switch_nodes_internaly(self, index1, index2):
        temp = self.route[index1]
        self.route[index1] = self.route[index2]
        self.route[index2] = temp

    def get_route(self):
        return self.route
