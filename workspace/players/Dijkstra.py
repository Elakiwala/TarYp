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
        print("PREPROCESS")
        # Get the initial location of the player
        print("Debut initial_location")
        initial_location = game_state.player_locations[self.name]
        print("Fin initial_location")
        # Get the location of the cheese
        print("Debut cheese_location")
        cheese_location = game_state.cheese[0]
        print("Fin cheese_location")
        # Perform a Dijkstra     traversal from the initial location
        print("Debut traversal")
        routing_table = self.traversal(maze, initial_location)
        print("Fin traversal")
        # Find the route from the initial location to the cheese location
        print("Debut find_route")   
        route = self.find_route(routing_table, initial_location, cheese_location)
        print("Fin find_route")
        # Convert the route to actions
        print("Debut actions")
        self.actions = maze.locations_to_actions(route)
        print("Fin actions")
        # Print phase of the game
        print("Preprocessing")

    #############################################################################################################################################
    
    def add_or_replace2(self: Self, queue: Dict[Integral, Any], key:Integral, value:Integral)->Dict[Integral, Integral]:
        """
            This method adds or replaces an element in a min-heap.
            In:
                * queue:  une liste initiale qui va contenir les couples (key,value).
                * key:   The key of the element to add or replace.
                * value: The value of the element to add or replace.
            Out:
                * List.
        """
        # If the key is already in the heap, we remove the previous element if the new value is lower
        if (key in queue):
            if value < queue[key]:
                queue[key]=value

        # We add the new elements
        else:
            queue[key] = value 
        return queue

    def remove (self: Self, queue: Dict[Integral, Any])->Tuple:

        # We find the element with the smallest value
        min_index = None
        min_kay = None
        for key, value in queue.items():
            if value is not None:
                if min_index is None or value < min_index:
                    min_index = value
                    min_kay = key

        # We remove the element with the smallest value
        if min_kay is not None:
            # Supprime l'élément ayant la plus petite valeur et retourne sa clé et sa valeur
            value = queue.pop(min_kay)
        return min_kay, value  
    
   
    def turn ( self:    Self,
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

    
    def traversal(self: Self, graph: Graph, source: Integral) -> Dict[Integral, Optional[Integral]]:
        #distances: Dict[Integral, int]
        #distances[source] = 0
        routing_table: Dict[Integral, Optional[Integral]] = {vertex: None for vertex in graph}
        min_heap: Dict[Integral, int] = {source: 0}

        while min_heap:
            current_vertex, current_distance = self.remove(min_heap)
            for neighbor in graph.get_neighbors(current_vertex):
                distance = current_distance + graph.get_weight(current_vertex, neighbor)
                #if distance < distances[neighbor]:
                #    distances[neighbor] = distance
                routing_table[neighbor] = current_vertex
                self.add_or_replace2(min_heap, neighbor, distance)

        return routing_table

    
    def find_route ( self:          Self,
                 min_heap:      Dict[Integral, Optional[Integral]],
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
        print("Debut find_route")
        route = []
        current = target
        while current is not None:
            route.append(current)
            current = route[current]

        route.reverse()
        return route
    
#####################################################################################################################################################
#####################################################################################################################################################

if __name__=="__main__":
    heap = {}
    player = Dijkstra()
    heap = player.add_or_replace2(heap, 1, 50)
    print(heap)
    heap2 = {1: 50, 2: 22, 3:90}
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