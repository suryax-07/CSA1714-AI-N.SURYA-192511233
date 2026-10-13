
import heapq

graph = {
    'S': {'A': 1, 'B': 4},
    'A': {'C': 2, 'D': 5},
    'B': {'D': 1},
    'C': {'G': 5},
    'D': {'G': 2},
    'G': {}
}

heuristic = {
    'S': 7,
    'A': 6,
    'B': 3,
    'C': 5,
    'D': 2,
    'G': 0
}

start = 'S'
goal = 'G'

queue = [(heuristic[start], 0, start, [start])]
best_cost = {start: 0}

while queue:
    f, g, node, path = heapq.heappop(queue)

    if node == goal:
        print("Path:", path)
        print("Total Cost:", g)
        break

    if g != best_cost[node]:
        continue

    for neighbour, cost in graph[node].items():
        new_cost = g + cost

        if neighbour not in best_cost or new_cost < best_cost[neighbour]:
            best_cost[neighbour] = new_cost
            new_path = path + [neighbour]
            f = new_cost + heuristic[neighbour]

            heapq.heappush(
                queue, (f, new_cost, neighbour, new_path)
            )
