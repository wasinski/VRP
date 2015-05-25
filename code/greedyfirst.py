class GreedyFirst(object):
    # TODO: checking if the next node has the same demand, and if it is closer, if yes set it!
    def run(instance):
        instance.network.sort_network_by_demand()
        network = instance.network
        fleet = instance.fleet
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
            vehicle.route.insert(0, depot)
            vehicle.route.append(depot)
        return instance
