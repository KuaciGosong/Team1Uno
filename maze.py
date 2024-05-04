import random
import numpy as np
from collections import deque

# Maze generation
UKURAN = (10, 5)
def generate_maze():
    global generated_maze
    generated_maze = None
    while generated_maze is None or not bfs(generated_maze, (0, 0), (UKURAN[0] - 1, UKURAN[1] - 1)):
        generated_maze = np.ones(UKURAN, dtype=int)
        generated_maze[0][0] = 0
        generated_maze[UKURAN[0] - 1][UKURAN[1] - 1] = 0
        dfs(generated_maze, (0, 0), set())
        
        # Randomly place walls while ensuring there's always a path from start to end
        random.seed()
        rows, cols = UKURAN
        for x in range(rows):
            for y in range(cols):
                if (x, y) != (0, 0) and (x, y) != (rows - 1, cols - 1):
                    generated_maze[x][y] = random.randint(0, 1)
    return generated_maze

# Maze generation text
def generate_maze_text(maze):
    rows, cols = UKURAN
    teks = ""

    # Dictionary untuk menentukan karakter representasi
    char_map = {
        0: " ",    # Jalur
        1: "██",   # Dinding
        "start": "🟢",  # Titik awal
        "end": "🔴"     # Titik akhir
    }

    # Baris labirin
    maze_row = ""

    # Baris labirin bagian atas
    top_row = "┌" + "─" * (cols * 2 - 1) + "┐\n"

    teks += top_row

    for x in range(rows):
        for y in range(cols):
            if y == 0:
                maze_row += "│"  # Awal baris
            if (x, y) == (0, 0):
                maze_row += char_map["start"]
            elif (x, y) == (rows - 1, cols - 1):
                maze_row += char_map["end"]
            else:
                maze_row += char_map[maze[x][y]]
            if maze[x][y] == 1:
                maze_row += "██"  # Dinding
            else:
                maze_row += "  "  # Jalur
            if y == cols - 1:
                maze_row += "│"  # Akhir baris
        teks += maze_row + "\n"

        if x != rows - 1:
            teks += "│" + " " * (cols * 2 - 1) + "│\n"  # Baris kosong

        maze_row = ""  # Reset baris labirin

    # Baris labirin bagian bawah
    bottom_row = "└" + "─" * (cols * 2 - 1) + "┘\n"

    teks += bottom_row

    return teks

# Depth-First Search (DFS) algorithm
def dfs(maze, node, visited):
    visited.add(node)
    x, y = node
    maze[x][y] = 0  # Change visited point to wall
    rows, cols = UKURAN
    neighbors = [(x+dx, y+dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] if 0 <= x+dx < rows and 0 <= y+dy < cols and maze[x+dx][y+dy]]
    for neighbor in neighbors:
        if neighbor not in visited:
            dfs(maze, neighbor, visited)

# Breadth-First Search (BFS) algorithm
def bfs(maze, awal, akhir):
    rows, cols = UKURAN
    antrian = deque([awal])
    visited = set([awal])  # Initialize visited set with the start node
    parent = {}

    while antrian:
        node = antrian.popleft()
        x, y = node
        
        # Check if the current node is the target node
        if node == akhir:
            path = []
            while node != awal:
                path.append(node)
                node = parent[node]
            path.append(awal)
            path.reverse()
            return path
        
        # Explore neighbors
        neighbors = [(x+dx, y+dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] if 0 <= x+dx < rows and 0 <= y+dy < cols]
        for neighbor in neighbors:
            nx, ny = neighbor
            if neighbor not in visited and not maze[nx][ny]:  # Check if neighbor is not visited and not a wall
                antrian.append(neighbor)
                parent[neighbor] = node
                visited.add(neighbor)  # Add visited status here to avoid re-visiting
                if neighbor == akhir:
                    # If the target node node is found during exploration, return the path
                    path = []
                    while neighbor != awal:
                        path.append(neighbor)
                        neighbor = parent[neighbor]
                    path.append(awal)
                    path.reverse()
                    return path
    return None
