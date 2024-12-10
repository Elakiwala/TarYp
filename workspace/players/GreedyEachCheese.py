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

class GreedyEachCheese(Player):

    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:

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
        self.current_target: Optional[Any] = None
        # Print phase of the game
        print("Constructor")

    def preprocessing(self, maze: Maze, game_state: GameState) -> None:
        print("Preprocessing phase")

        # Initialisation des paramètres
        initial_location = game_state.player_locations[self.name]
        cheese_location = game_state.cheese

        print("Initialisation du graphe")
        graphe = self.ajout_sommet2({}, initial_location, cheese_location)

        print("Ajout des pondérations")
        graphe, routing_table = self.ponderation3(maze, graphe, initial_location, cheese_location)
        print(graphe)
        print(f"routing_table: {routing_table}")
        print("Calcul de toutes les permutations")

        print("Recherche du meilleur chemin")
        local_best_path = self.greedy(cheese_location, initial_location, graphe)
        print(local_best_path)
        print("Conversion du meilleur chemin en route détaillée")

        route = self.find_route(routing_table, initial_location, local_best_path[0])
        print("route", route)
        print("Conversion de la route en actions")
        self.actions = maze.locations_to_actions(route)
        self.current_target = local_best_path[0][-1] if local_best_path[0] else None

        # Print phase of the game
        print("Preprocessing")

    def turn(self: Self, maze: Maze, game_state: GameState) -> Action:
        print("Turn", game_state.turn)

        # Si la cible actuelle (self.current_target) a été capturée par un adversaire (elle n'est plus dans game_state.cheese), 
        # on doit recalculer le chemin.
        if self.current_target and self.current_target not in game_state.cheese:
            print(f"Target cheese {self.current_target} taken by opponent, recalculating path")
            initial_location = game_state.player_locations[self.name] #position actuelle du joueur
            cheese_location = game_state.cheese #les fromages qui restent dans le graphe

            graphe = self.ajout_sommet2({}, initial_location, cheese_location)
            graphe, routing_table = self.ponderation3(maze, graphe, initial_location, cheese_location)
            local_best_path = self.greedy(cheese_location, initial_location, graphe)
            route = self.find_route(routing_table, initial_location, local_best_path[0])
            self.actions = maze.locations_to_actions(route)
            self.current_target = local_best_path[0][-1] if local_best_path[0] else None

        if self.actions:
            action = self.actions.pop(0)
        else:
            action = Action.NOTHING
        return action

    def ajout_sommet2(self, graph: Dict, initial_location: Any, cheeses: List[Any]) -> Dict:
        graph[initial_location] = {}
        for cheese in cheeses:
            if cheese not in graph:
                graph[cheese] = {}
        return graph

    def ponderation3(
        self, maze: Maze, graph: Dict, initial_location: Any, cheeses: List[Any]
    ) -> Tuple[Dict, Dict]:
        metagraph = {}
        routing_tables = {}
        dijkstra = Dijkstra()

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

    def greedy(self, cheeses, initial_location, graph):
        visited = [initial_location]
        distance_totale = 0
        current_location = initial_location

        if any(cheese not in graph for cheese in cheeses):
            raise ValueError("Tous les fromages ne sont pas représentés dans le graphe.")

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
            distance_totale += min_distance
            current_location = next_cheese

        if len(visited) - 1 != len(cheeses):
            raise ValueError("Certains fromages n'ont pas pu être atteints, vérifiez le graphe.")

        return visited, distance_totale

    def find_route(self: Self, routing_table, source, path):
        """
        Cette fonction trouve le plus court chemin entre la source et la cible en utilisant
        la table de routage générée par Dijkstra.
        Args:
            routing_table: Dictionnaire contenant le prédécesseur de chaque nœud dans le plus
                    court chemin depuis la source.
            source: Le nœud de départ.
            target: Le nœud de destination.
        Returns:
            Une liste représentant le chemin du nœud source au nœud cible.
        """
        route: List[Any] = []
        dijkstra = Dijkstra()
        for i in range(len(path) - 1):
            route.append(dijkstra.find_route(routing_table[path[i]], path[i], path[i + 1]))
        chemin = []
        for i in range(len(route[0])):
            chemin.append(route[0][i])
        for i in range(1, len(route)):
            for j in range(1, len(route[i])):
                chemin.append(route[i][j])
        return chemin

    def postprocessing(self: Self, maze: Maze, game_state: GameState, stats: Dict[str, Any]) -> None:
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
        print("Postprocessing")
