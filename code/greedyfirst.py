class GreedyFirst(object):
    # TODO: checking if the next node has the same demand, and if it is closer, if yes set it!

    def __init__(self, instance):
        self.instance = instance

    def run(self):
        self.instance.network.sort_network_by_demand()
        network = self.instance.network
        fleet = self.instance.fleet
        # assigning nodes so that they fit the capacity restriction
        for node in network:
            if not node.visited:
                for vehicle in fleet:
                    try:
                        vehicle.add_node(node)
                        break
                    except ValueError:
                        continue
        # inserting start and end point of the route - the depot.
        depot = network.get_node(1)
        for vehicle in fleet:
            vehicle.route.insert_node(0, depot)
            vehicle.route.append_node(depot)
        return self.instance

    def sort_by_distance(fleet):
        for vehicle in fleet:
            pass
        pass

self.network.sort(key=lambda node: node.get_demand()
