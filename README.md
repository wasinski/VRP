This is an app for solving capacitated vehicle routing problem.


Current functionality:
* Importing TSPLIB euc2d format
* Branch and Bound algorithm
* TabuSearch based algorithm - *important*, read next paragraph
* All wrapped in a simple CLI interface


TabuSearch is based on a simple, not very efective local search heuristic, thing is that for now is more a LC-search than a meta-heuristic and it has difficulties in escaping local minima.


BnB should be working fine, was tested and found optimal solutions for instances up to 18 nodes and 3 vehicles (it took a *longer* while...)


*note* data files need to have the number of vehicles specified in the `name` atribute after a `k` letter, *e.g.* `E-n4-k3`.
