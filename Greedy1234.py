##########################################################################################
######################################################################## INFO ############
##########################################################################################

"""
    This file contains useful elements to define a particular player.
    In order to use this player, you need to instanciate it and add it to a game.
    Please refer to example games to see how to do it properly.
"""

##########################################################################################
###################################################################### IMPORTS ###########
##########################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *

# PyRat imports
from pyrat import Player, Maze, GameState, Action, Graph
from Dijkstra import Dijkstra
from itertools import permutations

##########################################################################################
###################################################################### CLASSES ###########
##########################################################################################

class Greedy(Player):

    """
        This player is basically a player that does nothing except printing the phase of the game.
        It is meant to be used as a template to create new players.
        Methods "preprocessing" and "postprocessing" are optional.
        Method "turn" is mandatory.
    """

    #######################################################################################
    #                                                                CONSTRUCTOR          #
    #######################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        None:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial
            values.
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
        self.actions: List = []
        # Print phase of the game
        print("Constructor")

    #########################################################################################
    #                                                               PYRAT METHODS           #
    ########################################################################################

    #@override
    def preprocessing(self, maze: Maze, game_state: GameState) -> None:
        print("Preprocessing phase")
        self.maze = maze
        self.dijkstra = Dijkstra()
        self.initial_location = game_state.player_locations[self.name]
        self.cheese_locations = list(game_state.cheese)

        # Créer un graphe pondéré entre le joueur et les fromages
        self.graph = self.ajout_sommet2({}, self.initial_location, self.cheese_locations)
        self.graph, self.routing_table = self.ponderation3(maze, self.graph, self.initial_location, self.cheese_locations)

    def turn(self, maze: Maze, game_state: GameState) -> Action:
        print(f"Turn {game_state.turn}")

        # Vérifie si des actions sont encore en cours
        if not self.actions:
            player_location = game_state.player_locations[self.name]
            cheeses = list(game_state.cheese)  # Liste dynamique des fromages restants

            if cheeses:
                # Générer un graphe mis à jour
                self.graph = self.ajout_sommet2({}, player_location, cheeses)
                self.graph, self.routing_table = self.ponderation3(maze, self.graph, player_location, cheeses)

                # Recherche du fromage le plus proche
                visited_path, _ = self.greedy(cheeses, player_location, self.graph)
                next_cheese = visited_path[1]  # Le premier fromage à visiter (après la position actuelle)
                print(f"Next target cheese: {next_cheese}")

                # Générer les actions pour atteindre le prochain fromage
                self.actions = maze.locations_to_actions(
                    self.find_route(self.routing_table, player_location, [next_cheese])
                )
                self.current_target = next_cheese

        # Exécute la prochaine action ou NOTHING s'il n'y a rien
        return self.actions.pop(0) if self.actions else Action.NOTHING

    def postprocessing(self, maze: Maze, game_state: GameState, stats: Dict[str, Any]) -> None:
        print("Postprocessing")

    # Fonctions réutilisées depuis Greedy
    def ajout_sommet2(self, graph: Dict, initial_location: Any, cheeses: List[Any]) -> Dict:
        graph[initial_location] = {}
        for cheese in cheeses:
            if cheese not in graph:
                graph[cheese] = {}
        return graph

    def ponderation3(self, maze: Maze, graph: Dict, initial_location: Any, cheeses: List[Any]) -> Tuple[Dict, Dict]:
        metagraph = {}
        routing_tables = {}
        dijkstra = self.dijkstra

        distance, routing_tab = dijkstra.traversal(maze, initial_location)
        metagraph[initial_location] = {c: distance[c] for c in cheeses}
        routing_tables[initial_location] = routing_tab

        for cheese_i in cheeses:
            distance, routing_tab = dijkstra.traversal(maze, cheese_i)
            if cheese_i not in metagraph:
                metagraph[cheese_i] = {}
            routing_tables[cheese_i] = routing_tab
            for cheese_j in cheeses:
                if cheese_i != cheese_j:
                    metagraph[cheese_i][cheese_j] = distance[cheese_j]

        return metagraph, routing_tables

    def greedy(self, cheeses: List[Any], initial_location: Any, graph: Dict) -> Tuple[List[Any], float]:
        visited = [initial_location]
        total_distance = 0
        current_location = initial_location

        while len(visited) <= len(cheeses):
            min_distance = float('inf')
            next_cheese = None

            for cheese, distance in graph[current_location].items():
                if cheese not in visited and distance < min_distance:
                    min_distance = distance
                    next_cheese = cheese

            if next_cheese is None:
                break

            visited.append(next_cheese)
            total_distance += min_distance
            current_location = next_cheese

        return visited, total_distance

    def find_route(self, routing_table: Dict, source: Any, path: List[Any]) -> List[Any]:
        route = []
        for i in range(len(path) - 1):
            route.append(self.dijkstra.find_route(routing_table[path[i]], path[i], path[i + 1]))
        chemin = []
        for segment in route:
            chemin.extend(segment)
        return chemin
