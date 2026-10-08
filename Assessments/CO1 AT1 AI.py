from collections import deque

grid_size = 5
start = (1, 1)
goal = (5, 5)

blocked = {
    (2, 2),
    (2, 3),
    (3, 3),
    (4, 2),
    (4, 4)
}

directions = [
    ("Up", (-1, 0)),
    ("Down", (1, 0)),
    ("Left", (0, -1)),
    ("Right", (0, 1))
]

def get_neighbors(node):
    r, c = node
    result = []

    for name, (dr, dc) in directions:
        nr = r + dr
        nc = c + dc

        if 1 <= nr <= grid_size and 1 <= nc <= grid_size:
            if (nr, nc) not in blocked:
                result.append((nr, nc))

    return result

def build_path(parent, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path

def bfs():
    queue = deque([start])
    visited = {start}
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return build_path(parent, goal)

def dfs():
    stack = [start]
    visited = {start}
    parent = {start: None}

    while stack:
        current = stack.pop()

        if current == goal:
            break

        neighbors = get_neighbors(current)

        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return build_path(parent, goal)

bfs_path = bfs()
dfs_path = dfs()

print("BFS Path:")
print(" -> ".join(str(x) for x in bfs_path))
print("BFS Cost:", len(bfs_path) - 1)

print()

print("DFS Path:")
print(" -> ".join(str(x) for x in dfs_path))
print("DFS Cost:", len(dfs_path) - 1)
