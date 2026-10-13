
distance = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

n = len(distance)
visited = [False] * n
path = [0]
visited[0] = True
total = 0
current = 0

while len(path) < n:
    nearest = -1
    minimum = float('inf')

    for city in range(n):
        if not visited[city] and distance[current][city] < minimum:
            minimum = distance[current][city]
            nearest = city

    path.append(nearest)
    visited[nearest] = True
    total += minimum
    current = nearest

total += distance[current][0]
path.append(0)

print("Tour:", path)
print("Total Distance:", total)
