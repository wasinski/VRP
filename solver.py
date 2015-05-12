import argparse
from CVRPSolver import supports, algorithms


class Solver(object):

    def __init__(self):
        pass


def main():
    argparser = argparse.ArgumentParser()
    argparser.parse_args()

    importer = supports.Importer()
    problem = importer.import_data("nazwa")

    solver = Solver()
    solver.solve()


if __name__ == '__main__':
    main()
