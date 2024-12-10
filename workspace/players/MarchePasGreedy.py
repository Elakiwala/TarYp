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

        # Initialisation des paramètres
        initial_location = game_state.player_locations[self.name]
        cheese_location = game_state.cheese
        print("cheeses_location", cheese_location)
        print("Initialisation du graphe")
        graphe = self.ajout_sommet2({}, initial_location, cheese_location)

        print("Ajout des pondérations")
        graphe, routing_table = self.ponderation3(maze, graphe, initial_location, cheese_location)
        print(graphe)
        print(f"routing_table: {routing_table}")
        print("Calcul de toutes les permutations")
        #all_paths = self.all_journeys_f(initial_location, cheese_location)

        print("Initialisation de la solution avec greedy")
        best_path, distance_tot = self.greedy(maze, graphe, initial_location, cheese_location)
        print("backtracking")
        #best_path, best_distance = self.backtracking_with_greedy(initial_location, cheese_location, graphe, best_path, best_distance)
        print("Conversion du meilleur chemin en route détaillée")

    
        route = self.find_route(routing_table, initial_location, best_path)
        print("route", route)
        print("Conversion de la route en actions")
        self.actions = maze.locations_to_actions(route)
        # Print phase of the game
        print("Preprocessing")

    #######################################################################################

    #@override
    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, defined in the Action
            enumeration.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Print phase of the game
        print("Turn", game_state.turn)
        # Extract the next action to perform from self.actions
        if self.actions:
            action = self.actions.pop(0)
        else:
            action = Action.NOTHING
        # Return an action
        return action

##############################################################################################
#STEP 1: Creation du méta graph
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
    
    def greedy(self, maze, graph, source, cheeses):
        dijkstra = Dijkstra()
        fromages_non_exploés = cheeses.copy()
        chemin_glouton = [source]
        noeud_courant = source
        while fromages_non_exploés:
            fromage_proche = None
            son_poids = float('inf')

            distances = dijkstra.traversal(maze, noeud_courant)[0]  
            print("distances", distances)
            for fromage in fromages_non_exploés:
                if distances[fromage] < son_poids:
                    fromage_proche = fromage
                    son_poids = distances[fromage]
            fromages_non_exploés.remove(fromage_proche)
            chemin_glouton.append(fromage_proche)
            noeud_courant = fromage_proche
        return chemin_glouton
    

    """def greedy(self, cheeses, initial_location, graph):
        min = float('inf')
        liste = []
        liste.append(initial_location)
        distance_totale = 0
        fromage = None
        for cheese in graph[initial_location]:
            if graph[initial_location][cheese] < min:
                min = graph[initial_location][cheese]
                fromage = cheese
        liste.append(fromage)
        distance_totale += min
        while len(liste)<len(cheeses)+1:
            min = float('inf')
            for cheese in graph[fromage]:
                if graph[fromage][cheese] < min and cheese not in liste:
                    min = graph[fromage][cheese]
                    fromage = cheese
            liste.append(fromage)
            distance_totale += min
        return liste, distance_totale"""

    def find_route(self: Self,
        routing_table,  # Table de routage générée par Dijkstra
        source,
        path,
        ):
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
            route.append(dijkstra.find_route(routing_table[path[i]], path[i], path[i+1]))
        chemin = []
        for i in range(len(route[0])):
            chemin.append(route[0][i])
        for i in range(1,len(route)):
            for j in range(1,len(route[i])):
                chemin.append(route[i][j])
        return chemin


    ###########################################################################################

    #@override
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


###########################################################################################
###########################################################################################