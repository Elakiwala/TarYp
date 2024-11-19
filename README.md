# Students

- Responsible of the codes: LANSALOT
- Responsible of the documentation:  KHOURY
- Responsible of the unit tests: HENRY

---

# Players

This project includes the implementation of a Dijkstra player, designed to calculate the shortest paths in a graph-based environment.

## Design Choices:
### Key Algorithms:
The Dijkstra algorithm was implemented to traverse graphs and compute the shortest paths. We followed the algorithm proposed in the course, utilizing min-heaps. To achieve this, we created new functions to ensure the proper functioning of the Dijkstra algorithm using heaps.  
We created the functions `add_or_replace2` and `remove` to enable the use of min-heaps, reducing runtime. Additionally, we rewrote the `traversal` and `find_route` functions.

### Functions Created:
- **`add_or_replace2`**: Optimizes the priority queue by adding new elements or replacing existing ones with lower values. This is essential for maintaining efficiency during traversal.
- **`remove`**: Extracts the element with the smallest value from the queue, a crucial operation for Dijkstra's algorithm.
- **`traversal`**: Implements the core of Dijkstra's algorithm to compute distances and routing tables.
- **`find_route`**: Builds the shortest path between a starting vertex and a destination vertex using the routing table.

### Complexity:
- **`add_or_replace2`**: \( O(1) \) for dictionary operations.
- **`remove`**: \( O(n) \) in the worst case, where \( n \) is the size of the queue.
- **`traversal`**: \( O(V + E \log V) \), where \( V \) is the number of vertices and \( E \) is the number of edges in the graph.
- **`find_route`**: \( O(n) \), where \( n \) is the length of the path.

### Defensive Programming:
- **`add_or_replace2`**: Handles cases where keys either exist or do not exist, ensuring the integrity of the queue.
- **`remove`**: Checks if the queue is empty to prevent runtime errors.
- **`traversal`**: Supports graphs with isolated vertices or unusual configurations, such as fully disconnected nodes.
- **`find_route`**: Includes checks for invalid routes (e.g., when the start and end vertices are not connected).

---

# Games

## Game Scripts:
The gaming environment follows the same process as those seen in class, using randomly generated mazes through the `BigHolesRandomMaze` class. These mazes test the player's ability to navigate complex, randomly generated graphs with varying parameters.

### Parameters Modified:
- **Maze size**: Ranges from very small (2x2) to very large (20x20) to test scalability.
- **Wall and cell percentages**: Adjusted to simulate mazes with different densities, ranging from sparse to nearly filled with obstacles. This affects player behavior (path choices) depending on the percentage of mud parameterized.

These adjustments ensure that the player is robust and performs well in various scenarios.

---

# Unit Tests

## Tests Designed:
### The `DijkstraTests` Class Includes:
- **`test_add_or_replace2`**: Validates the behavior of the priority queue management in different scenarios, including edge cases with negative and null values.
- **`test_remove`**: Tests the extraction of the minimum element and handles cases like identical values or empty queues.
- **`test_traversal`**: Ensures that graph traversal correctly computes distances and routing tables for various types of mazes.
- **`test_find_route`**: Ensures valid paths are found and handles edge cases like disconnected graphs or identical start and end vertices.

### Error Cases Tested:
- Invalid keys in `add_or_replace2` and `remove`.
- Empty graph configurations in `traversal`.
- Unreachable vertices in `find_route`.

### Missing Tests:
- Performance with extremely large graph sizes.
- Edge cases involving dynamic graph updates during traversal (e.g., adding/removing edges).

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