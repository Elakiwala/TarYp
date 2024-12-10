# Greedy

## Design Choices:
### Key Algorithm:
The `greedy()` function is a core part of the strategy used by the `GreedyEachCheese` player. This function implements a greedy algorithm to select the nearest cheese to the player's current location, at each step prioritizing the cheese that is closest, in terms of distance. The algorithm iterates through all available cheeses and always picks the one that is closest in the current context, without considering future implications. This approach simplifies decision-making but may not always lead to an optimal long-term strategy.

### Function:
- **`greedy(cheeses: List[Any], initial_location: Any, graph: Dict)`**: 
  - **Parameters**:
    - `cheeses`: A list of cheese locations that the player needs to collect.
    - `initial_location`: The player's current position in the maze.
    - `graph`: A dictionary representing the graph of locations and the distances between them.
  - **Returns**:
    - A tuple containing:
      - `visited`: A list of locations visited during the process, starting with the `initial_location` and including all cheeses visited.
      - `distance_totale`: The total distance traveled by the player while collecting the cheeses.

---

### Functionality:
The `greedy()` function works as follows:

1. **Initialization**: 
   - Starts with the player's initial location and an empty list of visited locations. The player's initial location is added to the visited list.
   - The total distance traveled is initialized to zero.

2. **Greedy Path Selection**:
   - At each step, the function iterates over all cheeses that haven't been visited yet.
   - It selects the nearest cheese (i.e., the one with the smallest distance from the current location), and this cheese is added to the visited list.
   - The total distance is updated by adding the distance to the selected cheese.

3. **Termination**:
   - The loop continues until all cheeses have been visited. The function checks if all cheeses are reachable and ensures that the distances between them are valid within the graph.
   - The function returns the list of visited locations (including the initial location and all cheeses in the order they were visited) and the total distance traveled.

### Complexity:
- **Time Complexity**: \( O(V) \), where \( V \) is the number of cheeses. The function performs a linear search over the cheeses to find the nearest one and updates the visited list.
  
- **Space Complexity**: \( O(V) \), where \( V \) is the number of cheeses. The function stores the visited locations and computes distances between them.

---

### Defensive Programming:
- **Check for missing cheeses**: 
  - The function raises a `ValueError` if any of the cheeses are not represented in the graph, ensuring that the algorithm does not attempt to find paths for unreachable cheeses.
  
- **Handling unreachable cheeses**: 
  - If the algorithm is unable to find a path to a cheese (i.e., all remaining cheeses are unreachable), the function ensures it will not continue and may raise an exception to indicate that the algorithm cannot proceed.

---

### Unit Tests:

#### Tests Designed:
- **`test_greedy_path_selection`**: Tests that the function selects the nearest cheese at each step and follows the greedy approach correctly.
- **`test_greedy_total_distance`**: Verifies that the total distance returned by the function is correct and reflects the path taken through the maze.
- **`test_greedy_with_unreachable_cheese`**: Tests the behavior when one or more cheeses are unreachable, ensuring that the function handles this scenario appropriately.
- **`test_greedy_complete_path`**: Ensures that the function correctly visits all cheeses in the maze and completes the path successfully.

#### Error Cases Tested:
- Invalid or missing cheeses in the graph.
- Scenarios where there are unreachable cheeses or disconnected parts of the maze.
  
---

### Additional Notes:
- The `greedy()` function is designed for simplicity and efficiency in small mazes where the immediate proximity of cheeses is the main concern.
- It does not consider the broader layout of the maze or future moves, which may lead to suboptimal behavior in larger or more complex environments.
- Future improvements could include using more advanced algorithms like A* or dynamic programming to evaluate longer-term paths rather than focusing solely on the nearest cheese.


# GreedyEachCheese

## Design Choices:
### Key Algorithm:
The `GreedyEachCheese` player uses a greedy strategy to collect all cheeses in the maze. The main algorithm selects one cheese at a time and always chooses the closest available cheese from the player's current location. It repeatedly performs this action until all cheeses are collected. The player recalculates the shortest path to the nearest cheese at every step, ensuring that each movement is as efficient as possible in the current context.

### Function:
- **`greedy(cheeses: List[Any], initial_location: Any, graph: Dict)`**:
  - **Parameters**:
    - `cheeses`: A list of cheese locations that the player needs to collect.
    - `initial_location`: The player's current position in the maze.
    - `graph`: A dictionary representing the graph of locations and the distances between them.
  - **Returns**:
    - A tuple containing:
      - `visited`: A list of locations visited during the process, starting with the `initial_location` and including all cheeses visited.
      - `distance_totale`: The total distance traveled by the player while collecting the cheeses.

---

### Functionality:
The `greedy()` function works as follows:

1. **Initialization**: 
   - The player starts at the `initial_location`, and the list of visited locations is initialized with the starting point. The total distance is set to 0.

2. **Greedy Path Selection**:
   - The function iterates over the available cheeses. For each unvisited cheese, it calculates the distance from the current location and chooses the nearest one.
   - Once the nearest cheese is selected, it is marked as visited, and the total distance is updated accordingly.

3. **Termination**:
   - The function continues until all cheeses have been visited. The list of visited locations and the total distance are returned.

### Complexity:
- **Time Complexity**: \( O(V) \), where \( V \) is the number of cheeses. Each iteration checks all unvisited cheeses to find the nearest one.
  
- **Space Complexity**: \( O(V) \), where \( V \) is the number of cheeses. The function maintains a list of visited locations and computes distances.

---

### Defensive Programming:
- **Check for missing cheeses**: 
  - If any cheeses are missing from the graph, a `ValueError` is raised to prevent further processing.

---

### Unit Tests:

#### Tests Designed:
- **`test_greedy_each_cheese`**: Verifies the behavior of the greedy algorithm when collecting cheeses one at a time.
- **`test_greedy_complete_path`**: Ensures that the function correctly visits all cheeses and calculates the path efficiently.
  
#### Error Cases Tested:
- Missing or unreachable cheeses in the graph.

---

### Additional Notes:
- The `GreedyEachCheese` algorithm does not consider the larger context of the maze, focusing only on immediate actions. This may lead to suboptimal strategies in more complex mazes.


# GreedyEachTurn

## Design Choices:
### Key Algorithm:
The `GreedyEachTurn` player follows a greedy approach in every turn, recalculating the best possible path to collect cheese at the start of each new round. The player selects the nearest cheese at every turn, ensuring that it always moves toward the closest target cheese. The strategy involves constant recalculation of the path to the nearest cheese, ensuring that the player adapts to any changes in the game state or the availability of cheeses.

### Functions:
- **`preprocessing(maze: Maze, game_state: GameState)`**: 
  - **Parameters**:
    - `maze`: The current maze environment.
    - `game_state`: The current state of the game, including player positions and cheese locations.
  - **Returns**:
    - No return value; updates the internal state of the player.

- **`turn(maze: Maze, game_state: GameState)`**:
  - **Parameters**:
    - `maze`: The current maze environment.
    - `game_state`: The current state of the game.
  - **Returns**:
    - `Action`: The action to be performed (e.g., move towards the next cheese).

---

### Functionality:
1. **Preprocessing**:
   - The `preprocessing` function initializes the player's state and sets up the graph representing the maze. It calculates the shortest paths using Dijkstra's algorithm and prepares the path to the first cheese.
   
2. **Turn Logic**:
   - In each turn, the `turn` function recalculates the best route to the nearest cheese based on the updated game state. The player re-evaluates the maze, recalculates distances, and selects the next cheese to collect.
   - If the current target cheese is taken by another player, the algorithm recalculates the path to the next available cheese.
   - The chosen action (move toward the next cheese) is returned.

### Complexity:
- **Time Complexity**: \( O(V + E \log V) \), where \( V \) is the number of vertices and \( E \) is the number of edges, for each recalculation of the path.
  
- **Space Complexity**: \( O(V) \), where \( V \) is the number of vertices.

---

### Defensive Programming:
- **Check for missing or taken cheeses**: 
  - The function handles cases where the target cheese has already been collected by another player, ensuring that the path is recalculated.
  
- **Handling changes in game state**: 
  - The function dynamically updates the game state, ensuring that any changes in the maze or cheese locations are reflected in the next action.

---

### Unit Tests:

#### Tests Designed:
- **`test_preprocessing`**: Ensures that the preprocessing phase correctly sets up the player's initial path and internal state.
- **`test_turn`**: Tests the player's behavior in each turn, ensuring the correct action is selected based on the current game state.
  
#### Error Cases Tested:
- Taken or missing cheeses in the game state.
- Incorrect path calculations or missing routes.

---

### Additional Notes:
- The `GreedyEachTurn` strategy ensures that the player always adapts to the current state of the game, recalculating paths as needed.
- The function uses a greedy approach, which may lead to suboptimal performance in more complex mazes or when future planning is needed.
