import heapq, time, csv
MAPS = {
    "open": [
        "S........",
        ".........",
        ".........",
        ".........",
        "........G"
    ],
    "cluttered": [
        "S..#.....",
        ".#.#.##..",
        "...#.....",
        "##...#...",
        ".....#..G"
    ],
    "dead_end": [
        "S....#...",
        "####.#.#.",
        ".....#.#.",
        ".#####.#.",
        ".......#G"
    ]
}

def locate(grid, symbol):
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == symbol:
                return (r, c)
def search(grid, method):
    start, goal = locate(grid, "S"), locate(grid, "G")
    rows, cols = len(grid), len(grid[0])
    def h(p):
        return abs(p[0]-goal[0]) + abs(p[1]-goal[1])
    frontier = [(0, 0, start)]
    parent, best = {}, {start: 0}
    generated, expanded, max_frontier = 1, 0, 1
    counter = 0
    while frontier:
        priority, _, node = heapq.heappop(frontier)
        g = best.get(node, float("inf"))
        if method == "greedy":
            # Greedy stores heuristic priority; stale entries are ignored by parent/best check.
            pass
        expanded += 1
        if node == goal:
            path, cur = [], node
            while cur != start:
                path.append(cur); cur = parent[cur]
            path.append(start); path.reverse()
            return {"found": True, "cost": len(path)-1, "expanded": expanded,
                    "generated": generated, "max_frontier": max_frontier, "path": path}
        r, c = node
        for nxt in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
            nr, nc = nxt
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] == "#":
                continue
            ng = g + 1
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                parent[nxt] = node
                counter += 1
                score = ng if method == "ucs" else h(nxt) if method == "greedy" else ng + h(nxt)
                heapq.heappush(frontier, (score, counter, nxt))
                generated += 1
        max_frontier = max(max_frontier, len(frontier))
    return {"found": False, "cost": None, "expanded": expanded,
            "generated": generated, "max_frontier": max_frontier, "path": []}
def main():
    rows = []
    for map_name, grid in MAPS.items():
        for method in ("ucs", "greedy", "astar"):
            t0 = time.perf_counter()
            result = search(grid, method)
            elapsed = (time.perf_counter()-t0)*1000
            row = {"map": map_name, "algorithm": method, **{k:v for k,v in result.items() if k != "path"},
                   "time_ms": round(elapsed, 4)}
            rows.append(row)
            print(row)
    with open("performance.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
if __name__ == "__main__": main()
