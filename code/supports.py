import re


def euclidian_distance(my_node1, my_node2):
    x1, y1 = my_node1
    x2, y2 = my_node2

    distance = ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
    return distance


def retrieve_minimal_fleet_size(instance_name):
    regexp = re.compile(r'k([0-9]+)$')
    match = regexp.search(instance_name)
    print (match)
    minimal_fleet_size = int(match.group(1))
    return minimal_fleet_size
