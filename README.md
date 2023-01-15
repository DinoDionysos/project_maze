requirements:

pip install mazelib
pip install matplotlib
pytorch für cuda: https://pytorch.org/get-started/locally/

solve_maze_with_bfs.py creates a maze, solves it with BFS and shows the path 
that it found
solve_maze_with_dfs.py creates a maze, solves it with DFS and shows the path 
that it found
solve_maze_with_ca.py creates a maze, solves it with a CA and shows the path 
that it found

solve_maze_with_bfs_visualized.py creates a maze, solves it with BFS and 
visualizes every step the algorithm takes in a GUI
solve_maze_with_dfs_visualized.py creates a maze, solves it with DFS and 
visualizes every step the algorithm takes in a GUI
solve_maze_with_ca_visualized.py creates a maze, solves it with a CA and 
visualizes every step the algorithm takes in a GUI

time_measurement.py lets DFS, BFS and CA solve a maze an measurese the time 
needed. Then shows the solution of each.

time_measurement_averaged.py solves 1000 randomly generated mazes with DFS, BFS 
and a CA and averages the time and steps needed to find the solution for each
algorithm.