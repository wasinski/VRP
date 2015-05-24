class GreedyFirst(object):
    # TODO: checking if the next node has the same demand, and if it is closer, if yes set it!

    def run(self, solution):
        network = solution.network.sort_network_by_demand()
        fleet = solution.fleet
        every_node_visited = False
        while not every_node_visited:
            for node in network:
                if not node.visited:
                    for vehicle in fleet:
                        try:
                            vehicle.add_node()
                            break
                        except ValueError:
                            continue
            for node in network:
                if node.visited:
                    every_node_visited = True
                    continue
                else:
                    every_node_visited = False
                    break

