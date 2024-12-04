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

##########################################################################################
###################################################################### CLASSES ###########
##########################################################################################

class Exhaustive(Player):

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
        print("initial_location")
        initial_location = game_state.player_locations[self.name]

        # Get the location of the cheeses
        print("cheese_location")
        cheese_location = game_state.cheese

        #Creation du nouveau graph
        print("graph")
        graphe: Dict(Any, Dict(Any, float)) = {}

        # Perform a DFS traversal from the initial location
        print("ajout_sommet")
        graphe = self.ajout_sommet2(graphe, initial_location, cheese_location)
        print("ponderation")
        graphe, routing_table = self.ponderation3(maze, graphe, initial_location, cheese_location)
        print(graphe)
        
        #Backtracking => Faire une routing table
        print("tsp Bruteforce")
        all_path = self.all_journeys_f(initial_location, cheese_location)
        print("tsp backtracking")
        best_path = self.best_journeys_f(initial_location, cheese_location, graphe)

        # Find the route from the initial location to the cheese location
        print("find_route")
        route = self.find_route(best_path, routing_table, initial_location)
        # Convert the route to actions
        print("locations_to_actions")

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

    def ajout_sommet(self, graph, initial_location, cheeses):
        #Ajout du sommet initial
        graph.add_vertex(initial_location)
        #Ajout des sommets des fromages
        n = len(cheeses)
        for i in range(n):
            graph.add_vertex(cheeses[i])
        return graph

    def ponderation(self, maze, graph, initial_location, cheeses):
        #Ajout des arêtes
        routing_tables = {}
        dijkstra = Dijkstra()
        n = len(cheeses)
        for i in range(n):
            distance, routing_tab = dijkstra.traversal(maze, initial_location)
            graph.add_edge(initial_location, cheeses[i], distance[cheeses[i]])
            routing_tables[cheeses[i]] = routing_tab
        return graph, routing_tables

    def ajout_sommet2(self, graph, initial_location, cheeses):
        #Ajout du sommet initial
        graph[initial_location] = {}
        #Ajout des sommets des fromages
        n = len(cheeses)
        for i in range(n):
            if cheeses[i] not in graph:
                graph[cheeses[i]] = {}
        return graph
    
    def ponderation2(self, maze, graph, initial_location, cheeses):
        #Ajout des arêtes
        metagraph = {}
        metagraph[initial_location] = {}
        routing_tables = {}
        dijkstra = Dijkstra()
        n = len(cheeses)
        distance, routing_tab = dijkstra.traversal(maze, initial_location)
        print(distance)
        print(len(cheeses))
        i =0
        for c in cheeses:
            metagraph[initial_location][c] = distance[c]
        for i in range(n):
            metagraph[initial_location][cheeses[i]] = distance[cheeses[i]]
            for j in range(i+1, n):
                distance, routing_tab = dijkstra.traversal(maze, cheeses[i])
                if cheeses[i] not in metagraph:
                    metagraph[cheeses[i]] = {}
                metagraph[cheeses[i]][cheeses[j]] = dijkstra.traversal(maze, cheeses[i])[0][cheeses[i+1]]
        return metagraph, routing_tab

    class Exhaustive(Player):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.actions: List[Action] = []
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

        print("Calcul de toutes les permutations")
        all_paths = self.all_journeys_f(initial_location, cheese_location)

        print("Recherche du meilleur chemin")
        best_path = self.best_journeys_f(initial_location, cheese_location, graphe)

        print("Conversion du meilleur chemin en route détaillée")
        route = self.find_route(best_path, routing_table, initial_location)

        print("Conversion de la route en actions")
        self.actions = maze.locations_to_actions(route)

    def turn(self, maze: Maze, game_state: GameState) -> Action:
        print("Turn", game_state.turn)
        return self.actions.pop(0) if self.actions else Action.NOTHING

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

    def all_journeys_f(self, source: int, cheeses: List[int]) -> List[List[int]]:
        all_journeys = []

        def perm_rec(next_cheeses: List[int], current_journey: List[int]):
            if not next_cheeses:
                all_journeys.append(current_journey)
            else:
                for i in range(len(next_cheeses)):
                    perm_rec(
                        next_cheeses[:i] + next_cheeses[i + 1 :],
                        current_journey + [next_cheeses[i]],
                    )

        perm_rec(cheeses, [source])
        return all_journeys

    def best_journeys_f(self, source: int, cheeses: List[int], graph: Dict) -> List[int]:
        best_journey = []
        best_length = float("inf")

        def perma_rec(next_cheeses: List[int], current_journey: List[int], current_length: int):
            nonlocal best_journey, best_length
            if not next_cheeses:
                if current_length < best_length:
                    best_length = current_length
                    best_journey = current_journey
            else:
                for i, next_vertex in enumerate(next_cheeses):
                    perma_rec(
                        next_cheeses[:i] + next_cheeses[i + 1 :],
                        current_journey + [next_vertex],
                        current_length + graph[current_journey[-1]][next_vertex],
                    )

        perma_rec(cheeses, [source], 0)
        return best_journey

    def find_route(
        self, best_path: List[Any], routing_table: Dict[Any, Dict[Any, List[Any]]], initial_location: Any
    ) -> List[Any]:
        path = [initial_location]
        for i in range(len(best_path) - 1):
            start, end = best_path[i], best_path[i + 1]
            path += routing_table[start][end][1:]  # Évite de répéter le sommet de départ
        return path

    def postprocessing(self, maze: Maze, game_state: GameState, stats: Dict[str, Any]) -> None:
        print("Postprocessing phase")


#STEP 2: TSP : bruteforce
    def all_journeys_f(self, source: int, cheeses: List[int]) -> List[List[int]]:
        all_journeys = []

        def perm_rec(next_cheeses: List[int], current_journey: List[int]):
            if len(next_cheeses) == 0:
                all_journeys.append(current_journey)
            else:
                n = len(next_cheeses)
                for i in range(n):
                    perm_rec(next_cheeses[:i] + next_cheeses[i+1:], current_journey + [next_cheeses[i]])

        perm_rec(cheeses, [source])
        return all_journeys

    
    def best_journeys_f(self, source: int, cheeses: List[int], graph) -> List[int]:
        best_journey:List[int] = []
        best_length = float('inf')

        def perma_rec(next_cheeses: List[int], current_journey: List[int], current_length: int):
            nonlocal best_journey, best_length

            # Si tous les sommets sont visités
            if len(next_cheeses) == 0:
                if current_length < best_length:
                    best_length = current_length
                    best_journey = current_journey
            else:
                # Explorer les permutations restantes
                for i in range(len(next_cheeses)):
                    next_vertex = next_cheeses[i]
                    perma_rec(
                        next_cheeses[:i] + next_cheeses[i+1:],
                        current_journey + [next_vertex],
                        current_length + graph[current_journey[-1]][next_vertex]
                    )

        # Démarrage de la récursion
        perma_rec(cheeses, [source], 0)
        return best_journey

#STEP 3: Obtention du chemin final
    #@override
    def find_route (self, best_path, best_journey, initial_location):
        #Obtention du chemin final
        path = [initial_location]
        for i in range(len(best_path) - 1):
            path += best_journey[best_path[i]][best_path[i + 1]]
        return path

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