# CSCS 161 Assignment #2 -- Zombie Apocalypse
# Name: David Tyler Gosbee
# Student number: 201905838

import matplotlib.pyplot as plt
import numpy
import networkx


def make_city(name, neighbours):
    """
    Create a city (implemented as a list).

    :param name: String containing the city name
    :param neighbours: The city's row from an adjacency matrix.

    :return: [name, Infection status (defailt value of False), List of neighbours]
    """

    return [name, False, list(numpy.where(neighbours == 1)[0])]


def make_connections(n, density=0.35):
    """
    This function will return a random adjacency matrix of size
    n x n. You read the matrix like this:

    if matrix[2,7] = 1, then cities '2' and '7' are connected.
    if matrix[2,7] = 0, then the cities are _not_ connected.

    :param n: number of cities
    :param density: controls the ratio of 1s to 0s in the matrix

    :returns: an n x n adjacency matrix
    """

    # Generate a random adjacency matrix and use it to build a networkx graph
    a = numpy.int32(numpy.triu((numpy.random.random_sample(size=(n, n)) < density)))
    G = networkx.from_numpy_matrix(a)

    # If the network is 'not connected' (i.e., there are isolated nodes)
    # generate a new one. Keep doing this until we get a connected one.
    # Yes, there are more elegant ways to do this, but I'm demonstrating
    # while loops!
    while not networkx.is_connected(G):
        a = numpy.int32(numpy.triu((numpy.random.random_sample(size=(n, n)) < density)))
        G = networkx.from_numpy_matrix(a)

    # Cities should be connected to themselves.
    numpy.fill_diagonal(a, 1)

    return a + numpy.triu(a, 1).T


# noinspection PyDefaultArgument
def set_up_cities(
        names=['City 0', 'City 1', 'City 2', 'City 3', 'City 4', 'City 5', 'City 6', 'City 7', 'City 8', 'City 9',
               'City 10', 'City 11', 'City 12', 'City 13', 'City 14', 'City 15']):
    """
    Set up a collection of cities (world) for our simulator.
    Each city is a 3 element list, and our world will be a list of cities.

    :param names: A list with the names of the cities in the world.

    :return: a list of cities
    """

    # Make an adjacency matrix describing how all the cities are connected.
    con = make_connections(len(names))

    # Add each city to the list
    city_list = []
    for n in enumerate(names):
        city_list += [make_city(n[1], con[n[0]])]

    return city_list


def draw_world(world):
    """
    Given a list of cities, produces a nice graph visualization. Infected
    cities are drawn as red nodes, clean cities as blue. Edges are drawn
    between neighbouring cities.

    :param world: a list of cities
    """

    G = networkx.Graph()

    bluelist = []
    redlist = []

    plt.clf()

    # For each city, add a node to the graph and figure out if
    # the node should be red (infected) or blue (not infected)
    for city in enumerate(world):
        if city[1][1]:
            G.add_node(city[0])
            bluelist.append(city[0])
        else:
            G.add_node(city[0], node_color='r')
            redlist.append(city[0])

        for neighbour in city[1][2]:
            G.add_edge(city[0], neighbour)

    # Lay out the nodes of the graph
    position = networkx.circular_layout(G)

    # Draw the nodes
    networkx.draw_networkx_nodes(G, position, nodelist=bluelist, node_color="b")
    networkx.draw_networkx_nodes(G, position, nodelist=redlist, node_color="r")

    # Draw the edges and labels
    networkx.draw_networkx_edges(G, position)
    networkx.draw_networkx_labels(G, position)

    # Force Python to display the updated graph
    plt.show()
    plt.draw()


def print_world(world):
    """
    In case the graphics don't work for you, this function will print
    out the current state of the world as text.

    :param world: a list of cities
    """

    print('{:15}{:15}'.format('City', 'Infected?'))
    print('------------------------')

    for city in world:
        print('{:15}{}'.format(city[0], city[1]))


def draw_pretty_histogram(times):
    """
    Create a pretty histogram showing a distribution of the number of times it
    took to get to the end of the world over the provided times.
    :param times: a list of the time to end of worlds. The distribution of
    these values will be created.
    """

    plt.hist(times)
    plt.xlabel('Time to End of World')
    plt.ylabel('Count')
    plt.title('Distribution of End of the World Times')
    plt.show()


# That's the end of the stuff provided for you.
# Put *your* code after this comment.
 
def zombify(cities, citiesno):
    """
    Zombifies the city specified by citiesno
    
    :param cities: a list of cities in the world
    :param citiesno: the integer of the city that will be zombified
    """
    
    # print("Zombified city ", citiesno)
    cities[citiesno][1] = True

def cure(cities, citiesno):
    """
    cures the city specified by citiesno
    
    :param cities: a list of cities in the world
    :param citiesno: the integer of the city that will be cured
    """
    
    # print("Cured city ", citiesno)
    cities[citiesno][1] = False
    
def sim_step(cities, p_spread, p_cure):
    """
    Performs a simulation step, where each city in the list has a chance to
    zombify other cities and cure itself based on the floats p_spread and p_cure
    
    :param cities: a list of cities in the world
    :param p_spread: the percent chance to spread ranging from 0 to 1
    :param p_cure: the percent chance to cure ranging from 0 to 1
    """
    # print("Time step")
    count = 0
    while count < len(cities):
        if cities[count][1] and numpy.random.rand() < p_spread:
            zombify(cities, cities[count][2][numpy.random.randint(0, len(cities[count][2]))])
        if cities[count][1] and numpy.random.rand() < p_cure and cities[count][0] != 'City 0':
            cure(cities, count)
        count += 1
        

def is_end_of_world(cities):
    """
    Checks the world to determine if all the cities are infected, returning
    a boolean with the current state of infection
    
    :param cities: a list of cities in the world
    """
    
    count = 0
    for city in cities:
        if city[1]:
            count += 1
        else:
            return False
    return True

def time_to_end_of_world(p_spread, p_cure):
    """
    Runs the simulation until all the cities are infected and returns the time
    it took to infect all the cities
    
    :param p_spread: the percent chance to spread ranging from 0 to 1
    :param p_cure: the percent chance to cure ranging from 0 to 1 
    """
    cities = set_up_cities()
    zombify(cities, 0)
    
    count = 0
    while not(is_end_of_world(cities)):
        sim_step(cities, p_spread, p_cure)
        count += 1
    
    return count

def end_world_many_times(n, p_spread, p_cure):
    """
    Runs the entire simulation multiple times and returns a list of the times
    
    :param n: The number of times to run the simulation
    :param p_spread: the percent chance to spread ranging from 0 to 1
    :param p_cure: the percent chance to cure ranging from 0 to 1
    """
    count = 0
    result = []
    while count < n:
        result.append(time_to_end_of_world(p_spread, p_cure))
        count += 1
    return result

def average_end_times(times):
    """
    Averages the times in the list and returns a float of the time
    
    :param times: A list containing the time that it took for the simulation to
    finish
    """
    count = 0
    total = 0
    for time in times:
        total += time
        count += 1
    return total / count

times = end_world_many_times(500, .5, 0)
draw_pretty_histogram(times)
print("The average time for the world to end: ", average_end_times(times))