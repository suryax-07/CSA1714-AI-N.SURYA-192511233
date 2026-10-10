
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

queue = [['S']]
visited = []

while queue:
    path = queue.pop(0)
    node = path[-1]

    if node == 'G':
        print("Shortest Path:", path)
        print("Path Cost:", len(path) - 1)
        break

    if node not in visited:
        visited.append(node)

        for neighbour in graph[node]:
            new_path = path + [neighbour]
            queue.append(new_path)
