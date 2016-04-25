'''
Genetic Algorithm - Travelling Salesman Problem

Ahmad Mel
ahmad.mel@e-campus.uab.cat

Python 2.7
'''

import random
import copy
import os
import time
import math
import csv

list_of_cities =[]

# probability that an individual Route will mutate
k_mut_prob = 0.6

# Number of generations to run for
k_n_generations = 100
# Population size of 1 generation (RoutePop)
k_population_size = 2000

# Size of the tournament selection. 
tournament_size = 7

# City class
class City(object):
    def __init__(self, name, distance_to=None):
        # Name and coordinates:
        self.name = name
        # Appends itself to the global list of cities:
        list_of_cities.append(self)
        # Creates a dictionary of the distances to all the other cities (has to use a value so uses itself - always 0)
        self.distance_to = {self.name:0.0}
        if distance_to:
            self.distance_to = distance_to

# Route Class
class Route(object):
    def __init__(self):
        self.route = sorted(list_of_cities, key=lambda *args: random.random())
        self.recalc_rt_len()

    def recalc_rt_len(self):
        # Zeroes its length
        self.length = 0.0
        # for every city in its route attribute:
        for city in self.route:
            # set up a next city variable that points to the next city in the list 
            # and wraps around at the end:
            next_city = self.route[self.route.index(city)-len(self.route)+1]
            # Uses the first city's distance_to attribute to find the distance to the next city:
            dist_to_next = city.distance_to[next_city.name]
            # adds this length to its length attr.
            self.length += dist_to_next

    def pr_cits_in_rt(self, print_route=False):
        '''
        self --> None

        Prints all the cities in the route, in the form <cityname1,cityname2,cityname3...>
        '''
        cities_str = ''
        for city in self.route:
            cities_str += city.name + ' -> '
        cities_str = cities_str[:-1] # chops off last comma
        if print_route:
            print('    ' + cities_str)

    def pr_vrb_cits_in_rt(self):
        '''
        self --> None

        Prints all the coordinate pairs of the cities in the route, in the form <|x,y|x,y|x,y|...>
        '''
        cities_str = '|'
        for city in self.route:
            cities_str += str(city.x) + ',' + str(city.y) + '|'
        print(cities_str)

    def is_valid_route(self):
        for city in list_of_cities:
            # helper function defined up to
            if self.count_mult(self.route,lambda c: c.name == city.name) > 1:
                return False
        return True

    # Returns the number of pred in sequence (duplicate checking.)
    def count_mult(self, seq, pred):
        return sum(1 for v in seq if pred(v))


# Contains a population of Route() objects
class RoutePop(object):
    def __init__(self, size, initialise):
        self.rt_pop = []
        self.size = size
        # If we want to initialise a population.rt_pop:
        if initialise:
            for x in range(0,size):
                new_rt = Route()
                self.rt_pop.append(new_rt)
            self.get_fittest()

    def get_fittest(self):
        '''
        self --> Route()

        Returns the two shortest routes in the population
        '''
        # sorts the list based on the routes' lengths
        sorted_list = sorted(self.rt_pop, key=lambda x: x.length, reverse=False)
        self.fittest = sorted_list[0]
        return self.fittest


# Class for bringing together all of the methods to do with the Genetic Algorithm
class GA(object):
    """
    For running the genetic algorithm.

    crossover(parent1, parent2): Returns a child route after breeding the two parent routes. 

    """
    def crossover(self, parent1, parent2):
        # new child Route()
        child_rt = Route()

        for x in range(0,len(child_rt.route)):
            child_rt.route[x] = None

        # Two random integer indices of the parent1:
        start_pos = random.randint(0,len(parent1.route))
        end_pos = random.randint(0,len(parent1.route))


        #### takes the sub-route from parent one and sticks it in itself:
        # if the start position is before the end:
        if start_pos < end_pos:
            # do it in the start-->end order
            for x in range(start_pos,end_pos):
                child_rt.route[x] = parent1.route[x] # set the values to eachother
        # if the start position is after the end:
        elif start_pos > end_pos:
            # do it in the end-->start order
            for i in range(end_pos,start_pos):
                child_rt.route[i] = parent1.route[i] # set the values to eachother


        # Cycles through the parent2. And fills in the child_rt
        # cycles through length of parent2:
        for i in range(len(parent2.route)):
            # if parent2 has a city that the child doesn't have yet:
            if not parent2.route[i] in child_rt.route:
                # it puts it in the first 'None' spot and breaks out of the loop.
                for x in range(len(child_rt.route)):
                    if child_rt.route[x] == None:
                        child_rt.route[x] = parent2.route[i]
                        break
        # repeated until all the cities are in the child route

        # returns the child route (of type Route())
        child_rt.recalc_rt_len()
        return child_rt

    def mutate(self, route_to_mut):
        '''
        Route() --> Route()

        Swaps two random indexes in route_to_mut.route. Runs k_mut_prob*100 % of the time
        '''
        # k_mut_prob %
        if random.random() < k_mut_prob:

            # two random indices:
            mut_pos1 = random.randint(0,len(route_to_mut.route)-1)
            mut_pos2 = random.randint(0,len(route_to_mut.route)-1)

            # if they're the same, skip to the chase
            if mut_pos1 == mut_pos2:
                return route_to_mut

            # Otherwise swap them:
            city1 = route_to_mut.route[mut_pos1]
            city2 = route_to_mut.route[mut_pos2]

            route_to_mut.route[mut_pos2] = city1
            route_to_mut.route[mut_pos1] = city2

        # Recalculate the length of the route (updates it's .length)
        route_to_mut.recalc_rt_len()

        return route_to_mut

    def mutate_2opt(route_to_mut):
        '''
        Route() --> Route()

        Swaps two random indexes in route_to_mut.route. Runs k_mut_prob*100 % of the time
        '''
        # k_mut_prob %
        if random.random() < k_mut_prob:

            for i in range(len(route_to_mut.route)):
                for ii in range(len(route_to_mut.route)): # i is a, i + 1 is b, ii is c, ii+1 is d
                    if (route_to_mut.route[i].distance_to[route_to_mut.route[i-len(route_to_mut.route)+1].name]
                     + route_to_mut.route[ii].distance_to[route_to_mut.route[ii-len(route_to_mut.route)+1].name]
                     > route_to_mut.route[i].distance_to[route_to_mut.route[ii].name]
                     + route_to_mut.route[i-len(route_to_mut.route)+1].distance_to[route_to_mut.route[ii-len(route_to_mut.route)+1].name]):

                        c_to_swap = route_to_mut.route[ii]
                        b_to_swap = route_to_mut.route[i-len(route_to_mut.route)+1]

                        route_to_mut.route[i-len(route_to_mut.route)+1] = c_to_swap
                        route_to_mut.route[ii] = b_to_swap 

            route_to_mut.recalc_rt_len()

        return route_to_mut

    def tournament_select(self, population):
        '''
        RoutePop() --> Route()

        Randomly selects tournament_size amount of Routes() from the input population.
        Takes the fittest from the smaller number of Routes(). 

        Principle: gives worse Routes() a chance of succeeding, but favours good Routes()
        '''

        # New smaller population (not intialised)
        tournament_pop = RoutePop(size=tournament_size,initialise=False)

        # fills it with random individuals (can choose same twice)
        for i in range(tournament_size-1):
            tournament_pop.rt_pop.append(random.choice(population.rt_pop))
        
        # returns the fittest:
        return tournament_pop.get_fittest()

    def evolve_population(self, init_pop):
        #makes a new population:
        descendant_pop = RoutePop(size=init_pop.size, initialise=True)

        # Elitism offset (amount of Routes() carried over to new population)
        elitismOffset = 0

        # if we have elitism, set the first of the new population to the fittest of the old
        descendant_pop.rt_pop[0] = init_pop.fittest
        elitismOffset = 1

        # Goes through the new population and fills it with the child of two tournament winners from the previous populatio
        for x in range(elitismOffset,descendant_pop.size):
            # two parents:
            tournament_parent1 = self.tournament_select(init_pop)
            tournament_parent2 = self.tournament_select(init_pop)

            # A child:
            tournament_child = self.crossover(tournament_parent1, tournament_parent2)

            # Fill the population up with children
            descendant_pop.rt_pop[x] = tournament_child

        # Mutates all the routes (mutation with happen with a prob p = k_mut_prob)
        for route in descendant_pop.rt_pop:
            if random.random() < 0.3:
                self.mutate(route)

        # Update the fittest route:
        descendant_pop.get_fittest()

        return descendant_pop

class App(object):
    """
    Runs the application
    """
    def __init__(self,n_generations,pop_size):
        '''
        Initiates an App object to run for n_generations with a population of size pop_size
        '''

        self.n_generations = n_generations
        self.pop_size = pop_size

        # Once all the cities are defined, calcualtes the distances for all of them.
        # for city in list_of_cities:
        #     city.calculate_distances()


	print "Calculating GA_loop"
	self.GA_loop(n_generations,pop_size)

    def GA_loop(self,n_generations,pop_size):
        # takes the time to measure the elapsed time
        start_time = time.time()

        # Creates the population:
        print "Creates the population:"
        the_population = RoutePop(pop_size, True)
        print "Finished Creation of the population"

        # gets the best length from the first population (no practical use, just out of interest to see improvements)
        initial_length = the_population.fittest.length

        # Creates a random route called best_route. It will store our overall best route.
        best_route = Route()

        # Main process loop (for number of generations)
        for x in range(1,n_generations):
            # Evolves the population:
            the_population = GA().evolve_population(the_population)

            # If we have found a new shorter route, save it to best_route
            if the_population.fittest.length < best_route.length:
                # set the route (copy.deepcopy because the_population.fittest is persistent in this loop so will cause reference bugs)
                best_route = copy.deepcopy(the_population.fittest)

            # Prints info to the terminal:
            print('Generation {0} of {1}'.format(x,n_generations))
            print('Current fittest has length {0:.2f}'.format(the_population.fittest.length))
            the_population.fittest.pr_cits_in_rt()
            print(' ')
            
        # takes the end time of the run:
        end_time = time.time()

        # Prints final output to terminal:
        print('Finished evolving {0} generations.'.format(n_generations))
        print("Elapsed time was {0:.1f} seconds.".format(end_time - start_time))
        print(' ')
        print('Initial best distance: {0:.2f}'.format(initial_length))
        print('Final best distance:   {0:.2f}'.format(best_route.length))
        print('The best route went via:')
        best_route.pr_cits_in_rt(print_route=True)

if __name__ == '__main__':
    """main unction to calculate the route for the data of the european cities"""
    try:
        start_time = time.time()

        f = open("eucit.csv", "r")
        
        cname = ["Amsterdam","Antwerp","Athens","Barcelona","Berlin","Bern","Brussels","Calais","Cologne","Copenhagen","Edinburgh","Frankfurt","Geneva","Genoa","Hamburg","Le Havre","Lisbon","London","Luxembourg","Lyon","Madrid","Marseille","Milan","Munich","Naples","Nice","Paris","Prague","Rome","Rotterdam","Strasbourg","Stuttgart","The Hague","Turin","Venice","Vienna","Zurich"]

        lines = int(f.readline())
        for i, li in enumerate(f.readlines(), start=1):
            os.system('cls' if os.name=='nt' else 'clear')
            print "Reading  '{}': {}/{} lines".format(f.name, i, lines)
            d = {}
            for j, line in enumerate(map(float, li.split()), start=1):
                d[cname[j-1]] = line
            tmp = City(cname[i-1], d)
        print("--- %s seconds ---" % str(time.time() - start_time))
        band = True
    except Exception, e:
        print e
        band = False
    if band:
        print "Searching for the best road"
        try:
            start_time = time.time()
            app = App(n_generations=k_n_generations,pop_size=k_population_size)
            print("--- Road found in %s seconds --- Happy Sales ---" % str(time.time() - start_time))
        except Exception, e:
            print "\n[ERROR]: %s\n" % e


