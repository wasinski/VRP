def main():
    import argparse
    import time

    from code import instance as inst
    from code import datamapping as dm
    from code import greedyfirst as gf
    from code import algorithm as a
    from code import baseobjects as bo

    from code import tabu
    from code import branchnbound as bnb

    argparser = argparse.ArgumentParser(description='CVRP_Solver')
    argparser.add_argument('-ProblemInstance', action='store', dest='ProblemInstance',
                            help='path to the instance you want to solve', required=True)
    arggroup = argparser.add_mutually_exclusive_group(required=True)
    arggroup.add_argument('-Tabu', action='store_true',
                           help='use tabu search algorithm')
    arggroup.add_argument('-BnB', action='store_true',
                           help='use branch and bound algorithm')

    args = argparser.parse_args()

    problem_path = args.ProblemInstance
    max_iterations = 100

    raw_data = dm.Importer()
    raw_data.import_data(problem_path)
    data = dm.DataMapper(raw_data)

    instance = inst.ProblemInstance(data)
    solution = a.Solution(instance)

    greedy_heuristic = gf.GreedyFirst(solution.solution)
    greedy_heuristic.run(sort=True)

    solution.value = solution.eval()

    value_from_greedy = solution.value
    if args.Tabu:
        tabu_search = tabu.TabuSearch(solution, max_iterations)
        print("Starting tabu search")
        start = time.process_time()
        tabu_search.run()
        end = time.process_time()
        print("time: " + str(end-start))
        print("initial value from greedy heuristic was: "+str(value_from_greedy))
        value_from_tabu = tabu_search.instance.value
        print("        value after running tabu search: "+str(value_from_tabu))
        print("routes:", end="")
        for i, vehicle in enumerate(tabu_search.instance.solution.fleet):
            print("\nvehicle "+ str(i+1)+": ", end="")
            for node in vehicle.route:
                print(node.id, end=", ")
        print("\n\n")

    elif args.BnB:
        bnb_algo = bnb.BranchNBound()
        bnb_algo.initialize(instance, value_from_greedy)
        print("Starting branch&bound with initial upper_bound from greedy heuristic")
        start = time.process_time()
        upper_bound, routes, edges, times_branched = bnb_algo.run()
        end = time.process_time()
        print("time: " + str(end-start))
        conv_routes = route_from_edges(routes)
        print("initial value: "+str(value_from_greedy))
        print("optimal value: "+str(upper_bound))
        print("routes:", end="")
        for i, route in enumerate(conv_routes):
            print("\nvehicle "+ str(i+1)+": ", end="")
            for node in route:
                print(node, end=", ")
        print("\n\n")


def route_from_edges(routes):
    DEPOT = 1
    converted_routes = []
    for route in routes:
        converted_route = []
        for edge in route:
            entry, exit = edge
            if entry not in converted_route:
                converted_route.append(entry)
            if exit not in converted_route or exit is DEPOT:
                converted_route.append(exit)
        converted_routes.append(converted_route)
    return converted_routes


if __name__ == '__main__':
    print("Please run CVRPSolver.py file insead of this one!")
