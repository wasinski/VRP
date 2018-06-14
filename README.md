This is an app for solving capacitated vehicle routing problem.

It begun as a project for my studies, however after few years I decided to
rewrite it and add some functionalities seeing that it has gathered some attention.

So if you are a student looking for a well-written CVRP implementation in Python, then look no further!

Current functionality:
* Importing TSPLIB euc2d format
* Branch and Bound algorithm
* TabuSearch based algorithm
* All wrapped in a simple CLI interface

In the near future:
* visualization of the solutions
* more heuristics

TabuSearch is based on a simple, not very efective local search heuristic, thing is that for now it's more a LC-search than a meta-heuristic *i.e.* it has difficulties in escaping local minima.

BnB should be working fine, was tested and found optimal solutions for instances up to 18 nodes and 3 vehicles (it took a *longer* while...)

*note*: data files need to have the number of vehicles specified in the `name` atribute after a `k` letter, *e.g.* `E-n4-k3`.
