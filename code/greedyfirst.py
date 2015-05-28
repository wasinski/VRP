from code import baseobjects


class GreedyFirst(object):
    # TODO: checking if the next node has the same demand, and if it is closer, if yes set it!

    def __init__(self, instance):
        self.instance = instance

    def run(self, sort=False):
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
            if sort:
                vehicle = self.sort_by_distance(vehicle)
            vehicle.route.append_node(depot)
        return self.instance

    def sort_by_distance(self, vehicle):
        sorted_route = baseobjects.Route()
        sorted_route.append_node(vehicle.route.pop_node_id(1))
        while(vehicle.route.route):
            source_id = sorted_route[-1].id
            destination_id = self.get_nearest_node(source_id, vehicle.route.route)
            sorted_route.append_node(vehicle.route.pop_node_id(destination_id))
        vehicle.set_route(sorted_route)
        return vehicle

    def get_nearest_node(self, source_id, present_nodes):
        minimum = 99999999999
        destination_id = None
        for destination in present_nodes:
            distance = self.instance.distance_matrix[source_id-1][destination.id-1]
            if 0 < distance < minimum:
                minimum = distance
                destination_id = destination.id
        return destination_id
