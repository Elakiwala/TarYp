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
        
        # Print phase of the game
        print("Preprocessing")

    #############################################################################################################################################
    @override
    def add_or_replace(self : Self,
                        key: Any,
                        value: int) -> None:
    
        # We check if the key is already in the heap
        index = None
        i = 0
        for i in range(len(self.elements)):
            if self.elements[i][0] == key:
                index = i
                break
            i += 1
        
        # If the key is already in the heap, we remove the previous element if the new value is lower
        add_new_element = True
        if index is not None:
            if value < self.elements[index][1]:
                del self.elements[index]
            else:
                add_new_element = False

        # We add the new element
        if add_new_element:
            self.elements.append((key, value))

    def add_or_replace2(self: Self, queue: List,key:int, value:int)->List:
        """
            This method adds or replaces an element in a min-heap.
            In:
                * queue:  une liste initiale qui va contenir les couples (key,value).
                * key:   The key of the element to add or replace.
                * value: The value of the element to add or replace.
            Out:
                * List.
        """
        for i, (k, v) in enumerate(queue):
            if k == key:
                if value < v:
                    queue[i] = (key, value)
                return
        queue.append((key, value))
    

    @override
    def remove (self: Self):

        # We find the element with the smallest value
        min_index = 0
        for i in range(1, len(self.elements)):
            if self.elements[i][1] < self.elements[min_index][1]:
                min_index = i

        # We remove the element with the smallest value
        key, value = self.elements[min_index]
        del self.elements[min_index]

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
              ) ->      Tuple[Dict[Integral, Integral], Dict[Integral, Optional[Integral]]]:

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
        distances = {vertex: float('inf') for vertex in graph}
        distances[source] = 0
        routing_table = {vertex: None for vertex in graph}
        min_heap = []
        min_heap.add_or_replace(source, 0)

        while not(len(min_heap)==0):
            current_distance, current_vertex = min_heap.remove()

            for neighbor, weight in graph[current_vertex]:
                distance = current_distance + weight

                min_heap.add_or_replace(neighbor, distance)

        return distances, routing_table

    @override
    def find_route ( self:          Self,
                 routing_table: Dict[Integral, Optional[Integral]],
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
        current = target

        while current is not None:
            route.append(current)
            current = routing_table[current]

        route.reverse()
        return route
    
#####################################################################################################################################################
#####################################################################################################################################################

if __name__=="__main__":
    heap = []
    print(heap.add_or_replace3([(1, 2), (2, 3)], 1, 1))
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