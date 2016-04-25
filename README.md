#Travelling Salesman Problem applied to European cities

The traveling salesman problem is a classic optimization problem that describes a salesman who must travel
between N cities. The order in which he does so is something he does not care about, as long as he visits
each one during his trip, and finishes where he was at first.  

Each city is connected to other close by cities, or nodes. The salesman wants to keep both the travel costs, as well as the distance he 
travels as low as possible.  

In our case we focus of course on the distance. Our main goal is to get the shortest distance of a salesman traveling between the European 
cities, using the genetic algorithm optimization method.  

We save the data containing the distance between european cities in a file [eucit.csv](eucit.csv).   
It will be imported by the program to configure the cities.  

To run the program simply type:
```
python tspeu.py
```

## Algorithm
Breeding is done by selecting a random range of cities from the first parent route, and placing it into an empty child route (in the same 
range). Gaps are then filled in, without duplicates, in the order they appear in the second parent route.  

Mutation is done by swapping two random cities. The algorithm is most effective with a reasonable high rate of mutation.  

Population evolution is achieved by filling a new population with new children from pairs of two tournament-
winning parents, and the fittest from the initial population will also be carried over.

## References
The distances were downloaded from [here](http://www.engineeringtoolbox.com/driving-distances-d_1029.html)
