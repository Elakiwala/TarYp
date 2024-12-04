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

class DFS (Player):

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
                 ) ->        None:

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
        self.actions = []
        # Print phase of the game
        print("Constructor")
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    #@Override
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
        initial_location = game_state.player_locations[self.name]

        # Get the location of the cheese
        cheese_location = game_state.cheese[0]

        # Perform a DFS traversal from the initial location
        distances, routing_table = self.traversal(maze, initial_location)

        # Find the route from the initial location to the cheese location
        route = self.find_route(routing_table, initial_location, cheese_location)

        # Convert the route to actions
        self.actions = maze.locations_to_actions(route)
        # Print phase of the game
        print("Preprocessing")

    #############################################################################################################################################

    #@Override
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
        # Extract the next action to perform from self.actions
        if self.actions:
            action = self.actions.pop(0)
        else:
            action = Action.NOTHING
        # Return an action
        return action

#############################################################################################################################################

    #@Override
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

   
    # Your code here
    #@override
    def traversal ( self:   Self,
                graph:  Graph,
                source: Integral
              ) ->      Tuple[Dict[Integral, Integral], Dict[Integral, Optional[Integral]]]:

        """
            This method performs a DFS traversal of a graph.
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

        # Initialize the distances and the routing table
        distances = {source: 0}
        routing_table = {source: None}

        # Initialize the stack
        stack = [source]

        # While the stack is not empty
        while stack:

            # Pop the last vertex
            vertex = stack.pop()
            voisin = graph.get_neighbors(vertex)

            # For each neighbor of the vertex
            for i in range(len(voisin)):

                # If the neighbor has not been explored yet
                if voisin[i] not in distances:

                    # Update the distance and the routing table
                    distances[voisin[i]] = distances[vertex] + 1
                    routing_table[voisin[i]] = vertex

                    # Push the neighbor to the stack
                    stack.append(voisin[i])

        # Return the distances and the routing table
        return distances, routing_table

    #@override
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

        # Your code here
        route = []
        current = target
        while current != source:
            route.append(current)
            current = routing_table[current]
        route.append(source)

        return route[::-1]


#####################################################################################################################################################
#####################################################################################################################################################
