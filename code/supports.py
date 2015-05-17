def euclidian_distance(my_node1, my_node2):
    x1, y1 = my_node1
    x2, y2 = my_node2

    distance = ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
    return distance
