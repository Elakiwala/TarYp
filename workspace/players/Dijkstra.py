#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a particular player.
    In order to use this player, you need to instanciate it and add it to a game.
    Please refer to example games to see how to do it properly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *
import heapq    

# PyRat imports
from pyrat import Player, Maze, GameState, Action, Graph

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Dijkstra (Player):

    """
        This player is basically a player that does nothing except printing the phase of the game.
        It is meant to be used as a template to create new players.
        Methods "preprocessing" and "postprocessing" are optional.
        Method "turn" is mandatory.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        Self:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
            This is useful not to declare again all the parent's attributes in the child class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        self.elements = []
        # Print phase of the game
        print("Constructor")
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    @override
    def preprocessing ( self:       Self,
                        maze:       Maze,
                        game_state: GameState,
                      ) ->          None:
        
        """
            This method redefines the method of the parent class.
            It is called once at the beginning of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * None.
        """
        
        # Get the initial location of the player
        initial_location = game_state.player_locations[self.name]

        # Get the location of the cheese
        cheese_location = game_state.cheese[0]

        # Perform a Dijkstra     traversal from the initial location
        distances, routing_table = self.traversal(maze, initial_location)[1], self.traversal(maze, initial_location)[0]

        # Find the route from the initial location to the cheese location
        route = self.find_route(routing_table, initial_location, cheese_location)

        # Convert the route to actions
        self.actions = maze.locations_to_actions(route)
        # Print phase of the game
        print("Preprocessing")

    #############################################################################################################################################
    @override
    def add_or_replace2(self: Self, queue: List, key:int, value:int)->List:
        """
            This method adds or replaces an element in a min-heap.
            In:
                * queue:  une liste initiale qui va contenir les couples (key,value).
                * key:   The key of the element to add or replace.
                * value: The value of the element to add or replace.
            Out:
                * List.
        """
        # We check if the key is already in the heap
        index = None
        for i in range(len(queue)):
            if queue[i][0] == key:
                index = i
                break
        
        # If the key is already in the heap, we remove the previous element if the new value is lower
        add_new_element = True
        if index is not None:
            if value < queue[index][1]:
                queue.pop(index)
            else:
                add_new_element = False

        # We add the new element
        if add_new_element:
            queue.append((key, value))
        return queue

    @override
    def remove (self: Self, queue: List)->Tuple:

        # We find the element with the smallest value
        min_index = 0
        for i in range(1, len(queue)):
            if queue[i][1] < queue[min_index][1]:
                min_index = i

        # We remove the element with the smallest value
        key, value = queue[min_index]
        del queue[min_index]

        # We return the key and value of the element removed
        return key, value


    @override
    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, defined in the Action enumeration.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Print phase of the game
        print("Turn", game_state.turn)

        # Return an action
        return Action.NOTHING

#############################################################################################################################################

    @override
    def postprocessing ( self:       Self,
                         maze:       Maze,
                         game_state: GameState,
                         stats:      Dict[str, Any],
                       ) ->          None:

        """
            This method redefines the method of the parent class.
            It is called once at the end of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
                * stats:      Statistics about the game.
            Out:
                * None.
        """

        # Print phase of the game
        print("Postprocessing")

    @override
    def traversal ( self:   Self,
                graph:  Graph,
                source: Integral
              ) ->      List[Tuple[int, int]]:

        """
            This method performs a Dijkstra traversal of a graph.
            It returns the explored vertices with associated 
            distances.
            It also returns the routing table, that is, the parent 
            of each vertex in the traversal.
            In:
                * self:   Reference to the current object.
                * graph:  The graph to traverse.
                * source: The source vertex of the traversal.
            Out:
                * distances:     The distances from the source to each explored vertex.
                * routing_table: The routing table, that is, 
                the parent of each vertex in the traversal (None for the source).
        """
        #distances = {vertex: float('inf') for vertex in graph}
        #distances[source] = 0
        #routing_table = {vertex: None for vertex in graph}
        min_heap = []
        min_heap = self.add_or_replace2(min_heap, source, 0)

        while not(len(min_heap)==0):
            current_vertex, current_distance = self.remove(min_heap)

            for neighbor in graph.get_neighbors(current_vertex):
                distance = current_distance + graph.get_weight(current_vertex, neighbor)
                min_heap = self.add_or_replace2(min_heap, neighbor, distance)

        return min_heap

    @override
    def find_route ( self:          Self,
                 min_heap:      List[int],
                 source:        Integral,
                 target:        Integral
               ) ->             List[Integral]:

        """
            This method finds the route from the source to the target using the routing table.
            In:
                * self:          Reference to the current object.
                * routing_table: The routing table.
                * source:        The source vertex.
                * target:        The target vertex.
            Out:
                * route: The route from the source to the target.
        """
        route = []
        road = []
        current = target
        for i in range(len(min_heap)):
            route.append(min_heap[i][0])

        while current is not None:
            road.append(current)
            current = route[current]

        road.reverse()
        return road
    
#####################################################################################################################################################
#####################################################################################################################################################

if __name__=="__main__":
    heap = []
    player = Dijkstra()
    heap = player.add_or_replace2(heap, 1, 50)
    print(heap)
    heap2 = [(1, 50), (2, 22), (3, 10)]
    player.remove(heap2)
    print(heap2)

    """# Create a min-heap
    heap = []
    
    # Add elements to the heap
    heap.add_or_replace("A", 50)
    heap.add_or_replace("B", 22)
    heap.add_or_replace("C", 10)

    # Show the elements of the heap
    print("Heap initial state:", self.elements)

    # Remove the element with the smallest value
    key, value = heap.remove()
    print("Removed:", key, value)
    print("Heap after remove():", heap.elements)

    # Add a new element to the heap
    heap.add_or_replace("B", 45)
    print("Heap after add_or_replace(B, 45):", heap.elements)

    # Add a new element to the heap
    heap.add_or_replace("A", 35)
    print("Heap after add_or_replace(A, 35):", heap.elements)

    # Remove the element with the smallest value
    key, value = heap.remove()
    print("Removed:", key, value)
    print("Heap after remove():", heap.elements)"""