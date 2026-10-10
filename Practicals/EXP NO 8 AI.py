
graph = {
    'S': ['A', 'B'],
    'A': ['C', 'D'],
    'B': ['E'],
    'C': ['F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': []
}

stack = [['S']]
visited = []

while stack:
    path = stack.pop()
    node = path[-1]

    if node == 'G':
        print("Path Found:", path)
        print("Path Cost:", len(path) - 1)
        break

    if node not in visited:
        visited.append(node)

        for neighbour in reversed(graph[node]):
            new_path = path + [neighbour]
            stack.append(new_path)
