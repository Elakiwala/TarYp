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
import heapq  # Importing heapq for min-heap operations

# PyRat imports
from pyrat import Player, Maze, GameState, Action, Graph

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Dijkstra(Player):

    """
        This player uses the Dijkstra algorithm to calculate the shortest path to a target.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        Self:
        """
            Constructor of the class.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.queue = []  # Priority queue to use as min-heap
        self.distances = {}
        self.routing_table = {}

        print("Constructor")

    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    @override
    def preprocessing (self: Self, maze: Maze, game_state: GameState) -> None:
        """
            Called once at the beginning of the game.
        """
        initial_location = game_state.player_locations[self.name]
        cheese_location = game_state.cheese[0]

        # Perform Dijkstra traversal from the initial location
        self.distances, self.routing_table = self.traversal(maze, initial_location)

        # Find the shortest route to the cheese
        route = self.find_route(self.routing_table, initial_location, cheese_location)
        self.actions = maze.locations_to_actions(route)

        print("Preprocessing")

    #############################################################################################################################################

    @override
    def add_or_replace(self: Self, key: Integral, value: int) -> None:
        """
            Adds or replaces an element in the priority queue.
            Ensures the element with minimum value is at the root of the heap.
        """
        # Check if the key already exists and replace if a lower value is found
        for i, (v, k) in enumerate(self.queue):
            if k == key:
                if value < v:
                    self.queue[i] = (value, key)
                    heapq.heapify(self.queue)  # Re-establish min-heap property
                return
        # Otherwise, add the new element
        heapq.heappush(self.queue, (value, key))

    @override
    def remove(self: Self) -> Tuple[Integral, int]:
        """
            Removes and returns the element with the smallest value in the priority queue.
        """
        value, key = heapq.heappop(self.queue)
        return key, value

    #############################################################################################################################################

    @override
    def traversal(self: Self, graph: Graph, source: Integral) -> Tuple[Dict[Integral, int], Dict[Integral, Optional[Integral]]]:
        """
            Performs Dijkstra's algorithm on the graph from a source vertex.
            Returns distances and routing_table.
        """
        self.distances = {vertex: float('inf') for vertex in graph}
        self.distances[source] = 0
        self.routing_table = {vertex: None for vertex in graph}
        
        # Initialize the priority queue
        self.queue = [(0, source)]  # (distance, vertex)

        while self.queue:
            current_vertex, current_distance = self.remove()

            # Skip if we've found a shorter path already
            if current_distance > self.distances[current_vertex]:
                continue

            for neighbor, weight in graph.get_neighbors(current_vertex):
                distance = current_distance + weight
                if distance < self.distances[neighbor]:  # Found a shorter path
                    self.distances[neighbor] = distance
                    self.routing_table[neighbor] = current_vertex
                    self.add_or_replace(neighbor, distance)

        return self.distances, self.routing_table

    @override
    def find_route(self: Self, routing_table: Dict[Integral, Optional[Integral]], source: Integral, target: Integral) -> List[Integral]:
        """
            Finds the shortest route from source to target using the routing table.
        """
        route = []
        current = target
        while current is not None:
            route.append(current)
            current = routing_table[current]
        route.reverse()
        return route

    #############################################################################################################################################

    @override
    def turn(self: Self, maze: Maze, game_state: GameState) -> Action:
        """
            Returns an action to perform at each turn of the game.
        """
        print("Turn", game_state.turn)
        if self.actions:
            return self.actions.pop(0)
        return Action.NOTHING

    #############################################################################################################################################

    @override
    def postprocessing(self: Self, maze: Maze, game_state: GameState, stats: Dict[str, Any]) -> None:
        """
            Called once at the end of the game.
        """
        print("Postprocessing")

#####################################################################################################################################################
#####################################################################################################################################################
