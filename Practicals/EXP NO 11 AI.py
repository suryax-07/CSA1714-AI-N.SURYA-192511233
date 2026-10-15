
colors = ["Red", "Green", "Blue"]

graph = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D"],
    "D": ["B", "C"]
}

assignment = {}

def solve(region):
    if region == len(graph):
        return True

    node = list(graph.keys())[region]

    for color in colors:
        if all(assignment.get(neighbour) != color
               for neighbour in graph[node]):
            assignment[node] = color

            if solve(region + 1):
                return True

            del assignment[node]

    return False

if solve(0):
    for region, color in assignment.items():
        print(region, ":", color)
else:
    print("No solution exists")
