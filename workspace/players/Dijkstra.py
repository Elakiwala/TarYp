#################################################################################################
########################################### INFO ################################################
#################################################################################################

"""
    This file contains useful elements to define a particular player.
    In order to use this player, you need to instanciate it and add it to a game.
    Please refer to example games to see how to do it properly.
"""

####################################################################################################
############################################ IMPORTS ###############################################
####################################################################################################
# External imports
from typing import Dict, Tuple, Optional, List
from numbers import Integral
from typing_extensions import cast, Any, Self

# PyRat imports
from pyrat import Player, Maze, GameState, Action, Graph


#############################################################################################
############################################ CLASSES ########################################
#############################################################################################

class Dijkstra (Player):

    """
        This player is basically a player that does nothing except printing the phase of the game.
        It is meant to be used as a template to create new players.
        Methods "preprocessing" and "postprocessing" are optional.
        Method "turn" is mandatory.
    """

    #########################################################################################
    #                                      CONSTRUCTOR                                      #
    #########################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        None:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object 
            and set their initial values.
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
        self.elements: List = []
        self.actions: List = []
        # Print phase of the game
        print("Constructor")

    ############################################################################################
    #                                       PYRAT METHODS                                      #
    ############################################################################################

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
        print("PREPROCESS")
        # Get the initial location of the player
        print("Debut initial_location")
        initial_location = game_state.player_locations[self.name]
        print("Fin initial_location")
        # Get the location of the cheese
        print("Debut cheese_location")
        cheese_location = game_state.cheese[0]
        print("Fin cheese_location")
        # Perform a Dijkstra traversal from the initial location
        print("Debut traversal")
        routing_table = self.traversal(maze, initial_location)[1]
        print("Fin traversal")
        # Find the route from the initial location to the cheese location
        print("Debut find_route")
        route = self.find_route(routing_table, initial_location, cheese_location)
        print("Fin find_route")
        # Convert the route to actions
        print("Debut actions")
        self.actions = maze.locations_to_actions(route)
        print("Fin actions")
        # Print phase of the game
        print("Preprocessing")

    #########################################################################################
    def add_or_replace2(self: Self,
                        queue: Dict[Integral, Any],
                        key:Integral, value:Integral
                    )->Dict[Integral, Integral]:
        """
            This method adds or replaces an element in a min-heap.
            In:
                * queue:  une liste initiale qui va contenir les couples (key,value).
                * key:   The key of the element to add or replace.
                * value: The value of the element to add or replace.
            Out:
                * List.
        """
        # If the key is already in the heap,
        # we remove the previous element if the new value is lower
        if key in queue:
            if value < queue[key]:
                queue[key]=value

        # We add the new elements
        else:
            queue[key] = value
        return queue

    def remove (self: Self, queue: Dict[Integral, Any])->Tuple:

        """
        Supprime et retourne l'élément ayant la plus petite valeur dans
        une file de priorité implémentée sous forme de dictionnaire.

        Cette méthode recherche l'élément avec la plus petite valeur dans
        le dictionnaire `queue`, le supprime, 
        et retourne sa clé ainsi que sa valeur associée. Si la file est vide ou
        ne contient que des valeurs `None`, 
        elle retourne `(None, None)`.

        Args:
            queue (Dict[Integral, Any]): Un dictionnaire représentant une file de
            priorité, où les clés sont de type entier 
                                        (`Integral`) et les valeurs peuvent être
                                        de n'importe quel type.

        Returns:
            Tuple[Optional[Integral], Optional[Any]]:
                - La clé (`min_key`) associée à la plus petite valeur.
                - La valeur (`min_index`) correspondant à cette clé.
                Si aucune clé valide n'existe, retourne `(None, None)`.
        """
        # We find the element with the smallest value
        min_index = None
        min_key = None
        for key, value in queue.items():
            if value is not None:
                if min_index is None or value < min_index:
                    min_index = value
                    min_key = key

        # We remove the element with the smallest value
        if min_key is not None:
            # Supprime l'élément ayant la plus petite valeur et retourne sa clé et sa valeur
            value = queue.pop(min_key)
            return min_key, value
        return None, None

    def turn ( self:    Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, 
            defined in the Action enumeration.
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

##########################################################################################

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

    def traversal(self: Self,
        graph: Graph,
        source: Integral
    ) -> Tuple[Dict[Integral, Integral], Dict[Integral, Optional[Integral]]]:

        """
        Effectue une traversée du graphe à partir d'un sommet source en
        utilisant l'algorithme de Dijkstra.

        Cette méthode calcule les distances minimales entre le sommet
        source et tous les autres sommets
        atteignables du graphe, ainsi qu'une table de routage indiquant
        le chemin le plus court vers chaque sommet.

        Args:
            graph: Le graphe à parcourir. Il doit fournir une méthode
            `get_neighbors(vertex)` qui retourne
                        les voisins d'un sommet, et une méthode `get_weight(u, v)`
                        qui retourne le poids de l'arête (u, v).
            source: Le sommet source à partir duquel la traversée commence. 
                            Il doit être de type entier (Integral).

        Returns:
            Tuple[Dict[Integral, Integral], Dict[Integral, Optional[Integral]]]: 
                - `distances`: Un dictionnaire associant à chaque sommet atteignable
                sa distance minimale depuis le sommet source.
                - `routing_table`: Un dictionnaire associant à chaque sommet atteignable
                son prédécesseur sur le chemin minimal. 
                La valeur `None` pour un sommet indique qu'il s'agit du sommet source.
        """
        # Vérification pour s'assurer que `source` est de type Integral
        if not isinstance(source, Integral):
            raise TypeError("source must be of type Integral")

        # Initialiser `distances`, `routing_table`, et `min_heap` avec le type `Integral`
        zero : Integral = cast(Integral, 0)
        distances: Dict[Integral, Integral] = {source: zero}
        routing_table: Dict[Integral, Optional[Integral]] = {source: None}
        min_heap: Dict[Integral, Integral] = {source: zero}

        while min_heap:
            current_vertex, current_distance = self.remove(min_heap)

            # Vérifiez que `current_vertex` et `current_distance` sont de type `Integral`
            inte_instance_vertex = isinstance(current_vertex, Integral)
            inte_instance_distance = isinstance(current_distance, Integral)
            if not inte_instance_vertex or not inte_instance_distance:
                raise TypeError("current_vertex and current_distance must be of type Integral")

            for neighbor in graph.get_neighbors(current_vertex):
                if not isinstance(neighbor, Integral):
                    raise TypeError("neighbor must be of type Integral")

                distance = current_distance + graph.get_weight(current_vertex, neighbor)

                if not isinstance(distance, Integral):
                    raise TypeError("distance must be of type Integral")

                # Si une distance plus courte vers `neighbor` est trouvée
                if neighbor not in distances or distance < distances[neighbor]:
                    distances[neighbor] = distance
                    routing_table[neighbor] = current_vertex
                    min_heap = self.add_or_replace2(min_heap, neighbor, distance)

        return distances, routing_table

    def find_route(self: Self,
        routing_table: Dict[Integral, Optional[Integral]],  # Table de routage générée par Dijkstra
        source: Integral,
        target: Integral
        ) -> List[Integral]:
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

        # Vérification pour s'assurer que `source` et `target` sont de type Integral
        if not isinstance(source, Integral) or not isinstance(target, Integral):
            raise TypeError("source and target must be of type Integral")

        # Initialiser `route` avec le type `Integral`
        route: List[Integral] = []
        current_vertex: Optional[Integral] = target  # Autorise `current` à être None

        # Trouver le chemin du nœud cible au nœud source
        while current_vertex is not None:
            route.insert(0, current_vertex)
            current_vertex = routing_table[current_vertex]

        return route
#######################################################################################
#######################################################################################

"""if __name__=="__main__":
    dijkstra = Dijkstra()

    # Exemple de file de priorité avec des entiers comme clés et valeurs
    queue: Dict[Integral | int, Integral | None | int] = {1: 5, 2: 3, 3: 8}

    # Suppression de l'élément avec la plus petite valeur
    key, value = dijkstra.remove(queue)
    print(f"Removed: key={key}, value={value}")  # Attendu : key=2, value=3
    print(f"Remaining queue: {queue}")  # Attendu : {1: 5, 3: 8}

    # Test avec une file vide
    queue = {}
    key, value = dijkstra.remove(queue)
    print(f"Removed from empty queue: key={key}, value={value}")  # Attendu : key=None, value=None

    # Test avec des valeurs `None` dans le dictionnaire
    queue = {1: None, 2: 4, 3: None}
    key, value = dijkstra.remove(queue)
    print(f"Removed with None values: key={key}, value={value}")  # Attendu : key=2, value=4
    print(f"Remaining queue: {queue}")  # Attendu : {1: None, 3: None}"""