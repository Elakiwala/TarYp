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

    def __init__(self):
        super().__init__()
        self.elements = []  # Initialize elements as an empty list for min-heap
        self.distances = {}  # To store shortest path distances
        self.routing_table = {}


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

    """
    @override
    def preprocessing(self: Self, maze: Maze, game_state: GameState) -> None:
        print("Starting preprocessing...")
        
        initial_location = game_state.player_locations[self.name]
        print(f"Initial location: {initial_location}")

        # Adjusted to use vertices and neighbors methods
        self.distances, self.routing_table = self.traversal(maze, initial_location)

        print("Preprocessing completed.")"""

    #############################################################################################################################################

    @override
    def add_or_replace(self: Self, key: Integral, value: int) -> None:
        for i, (v, k) in enumerate(self.queue):
            if k == key:
                if value < v:
                    self.queue[i] = (value, key)
                    heapq.heapify(self.queue)
                return
        heapq.heappush(self.queue, (value, key))

    @override
    def remove(self: Self) -> Tuple[Integral, int]:
        if not self.queue:
            return None, None
        value, key = heapq.heappop(self.queue)
        return key, value

    #############################################################################################################################################

    @override
    def traversal(self, maze: Maze, source: Integral) -> Tuple[Dict[Integral, Integral], Dict[Integral, Optional[Integral]]]:
        distances = {vertex: float('inf') for vertex in range(maze.nb_vertices)}
        distances[source] = 0
        routing_table = {vertex: None for vertex in range(maze.nb_vertices)}
        self.add_or_replace(source, 0)  # Ajoute la source dans le tas min avec une distance de 0

        while self.elements:
            current_vertex, current_distance = self.remove()

            # Exploration des voisins
            for neighbor, weight in maze.get_neighbors(current_vertex):
                distance = current_distance + weight

                # Si un chemin plus court est trouvé
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    routing_table[neighbor] = current_vertex
                    self.add_or_replace(neighbor, distance)

        return distances, routing_table


    
    @override
    def turn(self: Self, maze: Maze, game_state: GameState) -> Action:
        # Placeholder: the player does nothing for now
        print("Turn", game_state.turn)

        # Move towards the closest cheese
        cheeses = game_state.cheeses
        if len(cheeses) == 0:
            return Action.NOTHING  # No cheese available

        # Find the closest cheese using the distances computed during preprocessing
        closest_cheese = min(cheeses, key=lambda cheese: self.distances.get(cheese, float('inf')))
        route = self.find_route(self.routing_table, game_state.player_locations[self.name], closest_cheese)

        # Determine the next move to get closer to the cheese
        if len(route) < 2:
            return Action.NOTHING  # Already at the target or no path found

        next_move = route[1]
        current_position = game_state.player_locations[self.name]

        # Map next position to an action
        if next_move == (current_position[0] + 1, current_position[1]):
            return Action.RIGHT
        elif next_move == (current_position[0] - 1, current_position[1]):
            return Action.LEFT
        elif next_move == (current_position[0], current_position[1] + 1):
            return Action.DOWN
        elif next_move == (current_position[0], current_position[1] - 1):
            return Action.UP
        else:
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
