"""Day-4 challenge: enumerate belief-state representations for k candidate locations."""
from itertools import combinations
from math import comb


def enumerate_nonempty_beliefs(k):
    """Enumerate all non-empty subsets of k candidate junctions (worst-case belief space)."""
    locations = tuple(range(k))
    beliefs = []
    for r in range(1, k + 1):
        beliefs.extend(frozenset(c) for c in combinations(locations, r))
    return beliefs


def run():
    print('k | beliefs_without_sensor | beliefs_with_sensor | no-sensor guaranteed plan | sensor plan upper bound')
    for k in (2, 4, 8):
        all_beliefs = enumerate_nonempty_beliefs(k)
        sensor_beliefs = [frozenset({i}) for i in range(k)]
        # Symmetric cycle model: without observation, the controller cannot distinguish
        # the candidate positions; no common fixed action sequence guarantees docking.
        no_sensor_plan = 'not guaranteed'
        sensor_plan = k // 2  # maximum shortest-path distance on a k-node cycle
        print(f'{k} | {len(all_beliefs)} | {len(sensor_beliefs)} | {no_sensor_plan} | <= {sensor_plan} moves')

if __name__ == '__main__':
    run()
