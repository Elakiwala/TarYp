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

class GreedyEachTurn(Player):

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
        best_path = self.greedy(cheese_location, initial_location, graphe)
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

    def recalculate_path(self: Self, maze: Maze, game_state: GameState, current_location: Any) -> None:
        """
        Recalcule le chemin vers le fromage le plus proche et met à jour les actions.

        Args:
            maze (Maze): Le labyrinthe.
            game_state (GameState): L'état du jeu.
            current_location (Any): La position actuelle du joueur.
        """
        # Calculer le graphe et les tables de routage
        graph, routing_tables = self.ponderation3(maze, {}, current_location, list(game_state.cheese))
        # Trouver le fromage le plus proche
        best_path, _ = self.greedy(list(game_state.cheese), current_location, graph)
        self.indice_fromage_cible = best_path[1]  # Le prochain fromage ciblé
        # Convertir le chemin trouvé en actions
        route = self.find_route(routing_tables, current_location, best_path)
        self.actions = maze.locations_to_actions(route)
        print(f"New path calculated: {route}")


    #@override
    def turn(self: Self, maze: Maze, game_state: GameState) -> Action:
        """
        Méthode appelée à chaque tour de jeu. Retourne une action à effectuer.

        Args:
            maze (Maze): Objet représentant le labyrinthe.
            game_state (GameState): Objet représentant l'état du jeu.

        Returns:
            Action: Une action à effectuer parmi les possibles (MOVE, STOP, etc.).
        """
        # Affiche l'état actuel du tour
        print("Turn", game_state.turn)

        # Si des actions sont disponibles
        if self.actions:
            # Vérifier si le fromage cible est encore dans le labyrinthe
            if self.indice_fromage_cible in game_state.cheese:
                # Effectuer la prochaine action
                return self.actions.pop(0)
            else:
                # Si le fromage cible a disparu, recalculer la cible et le chemin
                if game_state.cheese:
                    print("Recalculating path as cheese was eaten...")
                    # Mise à jour de la position courante
                    current_location = game_state.player_locations[self.name]
                    # Mise à jour de l'indice du fromage cible et recalcul du chemin
                    self.recalculate_path(maze, game_state, current_location)
                    # Retourner la première action recalculée
                    return self.actions.pop(0)
                else:
                    # Si aucun fromage n'est disponible, arrêter
                    print("No more cheese left. Stopping.")
                    return Action.STOP
        else:
            # Si aucune action n'est encore définie
            if game_state.cheese:
                print("Calculating initial path...")
                # Mise à jour de la position courante
                current_location = game_state.player_locations[self.name]
                # Mise à jour de l'indice du fromage cible et calcul du chemin initial
                self.recalculate_path(maze, game_state, current_location)
                # Retourner la première action calculée
                return self.actions.pop(0)
            else:
                # Si aucun fromage n'est disponible, arrêter
                print("No more cheese left. Stopping.")
                return Action.STOP


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
    
    def greedy(self, cheeses, initial_location, graph):
        # Liste pour enregistrer les fromages visités
        visited = [initial_location]
        distance_totale = 0
        current_location = initial_location

        # Vérifier que le graphe contient tous les fromages
        if any(cheese not in graph for cheese in cheeses):
            raise ValueError("Tous les fromages ne sont pas représentés dans le graphe.")

        while len(visited) <= len(cheeses):
            min_distance = float('inf')
            next_cheese = None

            # Chercher le fromage le plus proche non visité
            for cheese, distance in graph[current_location].items():
                if cheese not in visited and distance < min_distance:
                    min_distance = distance
                    next_cheese = cheese

            # Si aucun fromage n'est trouvable, arrêter (sécurité pour les graphes non connexes)
            if next_cheese is None:
                break

            # Mise à jour de la liste des fromages visités, de la distance totale et de la position
            visited.append(next_cheese)
            distance_totale += min_distance
            current_location = next_cheese
        return visited, distance_totale



    def find_route(
    self: Self,
    routing_table: Dict[Any, Any],
    source: Any,
    path: List[Any],
) -> List[Any]:
        """
        Trouve le chemin complet entre une source et une cible en suivant les étapes définies dans un chemin.
        """
        route: List[Any] = []
        dijkstra = Dijkstra()
        
        # Vérification et transformation des clés si nécessaire
        path = [tuple(p) if isinstance(p, list) else p for p in path]
        
        for i in range(len(path) - 1):
            if path[i] not in routing_table or path[i + 1] not in routing_table[path[i]]:
                raise KeyError(f"Clé manquante pour {path[i]} ou {path[i + 1]} dans la table de routage")
            
            subroute = dijkstra.find_route(routing_table[path[i]], path[i], path[i + 1])
            route.append(subroute)
        
        # Aplatir la liste des routes pour obtenir une seule liste continue
        flattened_route = []
        for subroute in route:
            flattened_route.extend(subroute)
        
        return flattened_route


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