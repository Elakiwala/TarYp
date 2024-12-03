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
        graphe = Graph()

        # Perform a DFS traversal from the initial location
        print("ajout_sommet")
        graphe = self.ajout_sommet(graphe, initial_location, cheese_location)
        print("ponderation")
        graphe, routing_table = self.ponderation(maze, graphe, initial_location, cheese_location)

        #Backtracking => Faire une routing table
        print("tsp_backtracking")
        best_path = self.tsp_backtracking(graphe, initial_location)

        # Find the route from the initial location to the cheese location
        print("find_route")
        #route = self.find_route(best_path, routing_table, initial_location)
        # Convert the route to actions
        print("locations_to_actions")

        #self.actions = maze.locations_to_actions(route)
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
#STEP 1: Creation du méta-graph
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

#STEP 2: TSP : backtracking
    def tsp_backtracking(self, graph, start):
        def dfs(current, visited, path, distance):
            if len(visited) == len(graph.vertices):
                return path, distance

            min_distance = float('inf')
            best_path = []

            for neighbor in graph.vertices:
                if neighbor not in visited:
                    new_distance = distance + graph.get_weight(current, neighbor)
                    dfs(neighbor, visited + {neighbor}, path + [neighbor], new_distance)

                    if new_path_distance < min_distance:
                        min_distance = new_path_distance
                        best_path = new_path

            return best_path, min_distance
        
        dfs(start, {start}, [start], 0)
        return 0

#STEP 3: Obtention du chemin final
    #@override
    def find_route (self, best_path, routing_tables, initial_location):
        #Obtention du chemin final
        path = [initial_location]
        for i in range(len(best_path) - 1):
            path += routing_tables[best_path[i]][best_path[i + 1]]
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