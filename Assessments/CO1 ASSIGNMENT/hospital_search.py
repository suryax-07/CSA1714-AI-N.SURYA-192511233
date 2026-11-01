"""Hospital medicine-delivery robot: reproducible uninformed-search experiments.
Python 3; uses an implicit complete binary tree so million-state tests fit in memory.
"""
from collections import deque
from heapq import heappush, heappop
from time import perf_counter
import csv
import statistics
import os

SIZES = [1_000, 10_000, 100_000, 1_000_000]
REPEATS = 5
SEED = 2026

class HospitalGraph:
    """Implicit tree graph. Children of u are 2u+1 and 2u+2, when in range.
    Edge cost is 1 on the root-to-goal path and 100 on off-path edges.
    This deliberately models a weighted hospital where the direct corridor is cheap.
    """
    def __init__(self, n, goal=None):
        self.n = n
        self.start = 0
        self.goal = n - 1 if goal is None else goal
        # Ancestors of the goal identify the cheap route. O(log n) preprocessing.
        self.goal_ancestors = set()
        x = self.goal
        while x > 0:
            self.goal_ancestors.add(x)
            x = (x - 1) // 2
        self.goal_ancestors.add(0)

    def neighbors(self, u):
        if u > 0:
            yield (u - 1) // 2, self.edge_cost(u)
        left = 2 * u + 1
        right = left + 1
        if left < self.n:
            yield left, self.edge_cost(left)
        if right < self.n:
            yield right, self.edge_cost(right)

    def edge_cost(self, child):
        # A tree edge is cheap only if child is on the selected goal path.
        return 1 if child in self.goal_ancestors else 100


def reconstruct(parent, goal):
    path = [goal]
    while path[-1] in parent:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def bfs(graph, start=None, goal=None):
    start = graph.start if start is None else start
    goal = graph.goal if goal is None else goal
    stats = {'generated': 1, 'expanded': 0, 'max_frontier': 1}
    if start == goal:
        return [start], stats, 0
    q = deque([start]); seen = {start}; parent = {}
    while q:
        u = q.popleft(); stats['expanded'] += 1
        for v, _ in graph.neighbors(u):
            if v not in seen:
                seen.add(v); parent[v] = u; stats['generated'] += 1
                if v == goal:
                    stats['max_frontier'] = max(stats['max_frontier'], len(q) + 1)
                    return reconstruct(parent, goal), stats, len(reconstruct(parent, goal)) - 1
                q.append(v)
        stats['max_frontier'] = max(stats['max_frontier'], len(q))
    return None, stats, None


def recursive_dfs(graph, start=None, goal=None):
    start = graph.start if start is None else start
    goal = graph.goal if goal is None else goal
    stats = {'generated': 1, 'expanded': 0, 'max_frontier': 1}
    parent = {}; seen = {start}; active = 0; found = False
    def visit(u):
        nonlocal active, found
        active += 1; stats['max_frontier'] = max(stats['max_frontier'], active)
        stats['expanded'] += 1
        if u == goal:
            found = True; active -= 1; return True
        for v, _ in graph.neighbors(u):
            if v not in seen:
                seen.add(v); parent[v] = u; stats['generated'] += 1
                if visit(v):
                    active -= 1; return True
        active -= 1
        return False
    visit(start)
    if not found:
        return None, stats, None
    path = reconstruct(parent, goal)
    return path, stats, len(path) - 1


def uniform_cost_search(graph, start=None, goal=None):
    start = graph.start if start is None else start
    goal = graph.goal if goal is None else goal
    stats = {'generated': 1, 'expanded': 0, 'max_frontier': 1}
    if start == goal:
        return [start], stats, 0
    heap = [(0, 0, start)]; best = {start: 0}; parent = {}; closed = set(); tie = 1
    while heap:
        cost, _, u = heappop(heap)
        if u in closed or cost != best.get(u):
            continue
        closed.add(u)
        if u == goal:
            path = reconstruct(parent, goal)
            return path, stats, cost
        stats['expanded'] += 1
        for v, edge in graph.neighbors(u):
            new_cost = cost + edge
            if v not in closed and new_cost < best.get(v, float('inf')):
                best[v] = new_cost; parent[v] = u
                heappush(heap, (new_cost, tie, v)); tie += 1
                stats['generated'] += 1
        stats['max_frontier'] = max(stats['max_frontier'], len(heap))
    return None, stats, None

ALGORITHMS = [('BFS', bfs), ('Recursive DFS', recursive_dfs), ('Uniform Cost Search', uniform_cost_search)]

def run_experiments(out_dir='results'):
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for n in SIZES:
        graph = HospitalGraph(n)
        for name, algorithm in ALGORITHMS:
            times=[]; last=None
            for _ in range(REPEATS):
                t0 = perf_counter()
                path, stats, cost = algorithm(graph)
                times.append(perf_counter() - t0)
                last = (path, stats, cost)
            path, stats, cost = last
            depth = len(path) - 1 if path else -1
            # BFS/DFS return depth as their reported path cost; true weighted cost is
            # computed separately so the non-optimality of unweighted search is visible.
            true_cost = None
            if path:
                true_cost = sum(graph.edge_cost(v) for v in path[1:])
            rows.append({
                'states': n, 'algorithm': name, 'seed': SEED, 'runs': REPEATS,
                'nodes_generated': stats['generated'], 'nodes_expanded': stats['expanded'],
                'max_frontier': stats['max_frontier'], 'solution_depth': depth,
                'weighted_path_cost': true_cost, 'mean_time_seconds': statistics.mean(times),
                'stdev_time_seconds': statistics.pstdev(times),
                'optimal_weighted_path': (path is not None),  # unique path in this tree makes every found route optimal
                'reachable': path is not None,
            })
            print(f"N={n:>7} | {name:<18} generated={stats['generated']:>7} expanded={stats['expanded']:>7} frontier={stats['max_frontier']:>7} depth={depth:>2} cost={true_cost!s:<6} avg_s={statistics.mean(times):.6f}")
    path = os.path.join(out_dir, 'performance.csv')
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys())); writer.writeheader(); writer.writerows(rows)
    return rows


def edge_case_tests():
    cases=[]
    for label, n, start, goal in [
        ('reachable', 31, 0, 30),
        ('start_is_goal', 31, 7, 7),
        ('unreachable', 31, 0, 40),
    ]:
        g = HospitalGraph(n, goal=goal if goal < n else n-1)
        # For unreachable test, explicitly request a goal outside the graph.
        requested_goal = goal
        for name, fn in ALGORITHMS:
            path, stats, cost = fn(g, start=start, goal=requested_goal)
            cases.append((label, name, n, start, requested_goal, path, stats, cost))
    return cases

if __name__ == '__main__':
    run_experiments('results')
    print('\nEDGE CASES')
    for label, name, n, start, goal, path, stats, cost in edge_case_tests():
        print(f'{label:12} | {name:18} | start={start} goal={goal} | found={path is not None} | depth={len(path)-1 if path else -1} | generated={stats["generated"]} expanded={stats["expanded"]}')
