# Students

- Responsible of the codes: LANSALOT
- Responsible of the documentation:  KHOURY
- Responsible of the unit tests: HENRY

---

# Players

This project includes the implementation of a Dijkstra player, which is designed to calculate shortest paths in a graph-based environment.

## Choices made:

- ### Key Algorithms: 
    Dijkstra's algorithm was implemented for graph traversal and shortest path calculation.

- ### Functions created:
    - add_or_replace2: Optimizes the priority queue by adding new elements or replacing existing ones with a lower value. This is crucial for maintaining efficiency during traversal.
    - remove: Extracts the element with the minimum value from the queue, which is essential for Dijkstra's algorithm.
    - traversal: Implements the core of Dijkstra’s algorithm to calculate distances and routing tables.
    - find_route: Builds the shortest path between a start and an end vertex using the routing table.
- ### Complexity:
    - add_or_replace2: O(1) for dictionary operations.
    - remove: O(n) in the worst case, where n is the size of the queue.
    - traversal: O(V + E log V), where V is the number of vertices and E is the number of edges in the graph.
    - find_route: O(n), where n is the length of the path.
- ### Defensive programming:
    - add_or_replace2: Handles cases where keys already exist or do not exist. Ensures the queue's integrity.
    - remove: Checks for empty queues to avoid runtime errors.
    - traversal: Handles graphs with isolated vertices or unusual configurations like fully disconnected nodes.
    - find_route: Includes checks for invalid routes (e.g., when start and end vertices are not connected).

---

# Games

## Game scripts:
The game environment uses random mazes generated by the BigHolesRandomMaze class. These mazes test the player's ability to navigate complex, randomly generated graphs with varying parameters.

## Parameters changed:
Maze size: Ranges from very small (2x2) to very large (20x20) for scalability testing.
Wall and cell percentages: Adjusted to simulate mazes with different densities, from sparse to almost entirely filled with obstacles.
These adjustments ensure that the player is robust and performs consistently across a variety of scenarios.>

---

# Unit tests

## Tests designed:
- ### The DijkstraTests class includes:
    - test_add_or_replace2: Validates the behavior of the priority queue management under different scenarios, including edge cases with negative and zero values.
    - test_remove: Tests the extraction of the minimum element and handles cases like identical values or empty queues.
    - test_traversal: Verifies that the graph traversal correctly calculates distances and routing tables for various types of mazes.
    - test_find_route: Ensures that valid paths are found and handles edge cases like disconnected graphs or identical start and end vertices.

## Error cases tested:
- ### The DijkstraTests class includes:
    - Invalid keys in add_or_replace2 and remove.
    - Empty graph configurations in traversal.
    - Unreachable vertices in find_route.

## Missing tests:
- ### The DijkstraTests class doesn't includes:
    - Performance under extreme graph sizes.
    - Corner cases with dynamic graph updates during traversal (e.g., adding/removing edges).

---

# Utils

No additional files were provided in the utils directory for this project. However, future iterations could include utility functions for maze generation or result visualization.

---

# Documentation

The provided documentation is minimal and directly tied to the code comments. While functional, it could be expanded with:
    - Detailed explanations of the algorithms.
    - Visual diagrams of the graph traversal process in our projet context.

---

# Others

## Dependencies:
Python 3.x with the following libraries:
unittest: For running the unit tests.
random: For generating maze configurations.
Custom modules: Dijkstra, BigHolesRandomMaze, pyrat, and Graph.

## Additional notes:
The code is modular, making it easy to extend or adapt for new maze types or player strategies.
It performs well for small to medium graphs but could benefit from further optimization for larger datasets.