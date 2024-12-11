from pyrat import Player, Maze, GameState, Action
from collections import defaultdict
from typing import *
import numpy as np

class StrategicPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = []

    def preprocessing(self, maze: Maze, game_state: GameState) -> None:
        print("Preprocessing")

        # Initialisation des variables nécessaires
        self.maze = maze
        self.game_state = game_state
        self.player_position = game_state.player_locations[self.name]
        self.cheese_positions = list(game_state.cheese)
        self.opponent_positions = list(game_state.opponent_locations.values())

        # Calcul des zones à forte densité de fromages
        self.densest_zone = self._find_densest_zone(self.cheese_positions)

    def turn(self, maze: Maze, game_state: GameState) -> Action:
        print("Turn", game_state.turn)

        # Met à jour les positions des joueurs et fromages
        self.player_position = game_state.player_locations[self.name]
        self.cheese_positions = list(game_state.cheese)
        self.opponent_positions = list(game_state.opponent_locations.values())

        # Si aucune action pré-calculée n'est disponible, en calcule une nouvelle
        if not self.actions:
            self.actions = self._compute_next_actions()

        # Exécute la première action de la liste
        return self.actions.pop(0) if self.actions else Action.NOTHING

    def _compute_next_actions(self) -> List[Action]:
        """
        Calcule les prochaines actions en tenant compte des heuristiques.
        """
        # Liste des chemins possibles
        paths = []

        # Capture les fromages proches tout en allant vers la zone à forte densité
        for cheese in self.cheese_positions:
            if cheese not in self.densest_zone or self._is_opponent_closer(cheese):
                continue
            path = self.maze.shortest_path(self.player_position, cheese)
            if path:
                paths.append((path, len(path)))

        # Trie les chemins par longueur (plus court en premier)
        paths.sort(key=lambda x: x[1])

        # Retourne les actions correspondant au chemin le plus court
        return self.maze.locations_to_actions(paths[0][0]) if paths else [Action.NOTHING]

    def _find_densest_zone(self, cheese_positions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Identifie la zone contenant la plus grande densité de fromages.
        """
        density_map = defaultdict(int)

        # Calcule la densité locale pour chaque fromage
        for cheese in cheese_positions:
            for other_cheese in cheese_positions:
                if self.maze.distance(cheese, other_cheese) <= 3:
                    density_map[cheese] += 1

        # Trouve le fromage avec la densité maximale
        max_density = max(density_map.values())
        return [cheese for cheese, density in density_map.items() if density == max_density]

    def _is_opponent_closer(self, cheese: Tuple[int, int]) -> bool:
        """
        Vérifie si un adversaire est plus proche d'un fromage donné que le joueur.
        """
        player_distance = self.maze.distance(self.player_position, cheese)
        opponent_distances = [self.maze.distance(opponent, cheese) for opponent in self.opponent_positions]
        return any(opp_dist <= player_distance for opp_dist in opponent_distances)

    def postprocessing(self, maze: Maze, game_state: GameState, stats: Dict[str, Any]) -> None:
        print("Postprocessing")
