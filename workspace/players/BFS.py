# External imports
from typing import *
from typing_extensions import *
from numbers import *

# PyRat imports
from pyrat import Player, Maze, GameState, Action, Graph
from collections import deque

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class BFS (Player):
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
        self.actions = []
        # Print phase of the game
        print("Constructor")

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

    @override
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
        distances = {source: 0}
        routing_table = {source: None}
        queue = deque([source])

        while queue:
            current = queue.popleft()
            for neighbor in graph.get_neighbors(current):
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    routing_table[neighbor] = current
                    queue.append(neighbor)

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
            current = routing_table.get(current)

        route.reverse()
        return route
