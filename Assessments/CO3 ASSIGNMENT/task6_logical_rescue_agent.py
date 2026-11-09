import random

def make_world(n, seed):
    rng = random.Random(seed)
    hazards = {(r, c) for r in range(n) for c in range(n)
               if (r, c) not in {(0, 0), (n-1, n-1)} and rng.random() < 0.16}
    return hazards

def neighbours(cell, n):
    r, c = cell
    return [(rr, cc) for rr, cc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
            if 0 <= rr < n and 0 <= cc < n]

def run_agent(n, seed, cautious=True):
    hazards = make_world(n, seed)
    current = (0, 0)
    visited = {current}
    moves = 0
    entered = 0
    while current != (n-1, n-1) and moves < n*n*3:
        candidates = [x for x in neighbours(current, n) if x not in visited]
        if not candidates:
            break
        if cautious:
            # A cell is considered safe if no known hazard has been sensed nearby.
            safe = [x for x in candidates if all(h not in neighbours(x, n) for h in hazards if h in visited)]
            choice = safe[0] if safe else candidates[0]
        else:
            choice = random.Random(seed + moves).choice(candidates)
        current = choice
        visited.add(current)
        moves += 1
        if current in hazards:
            entered += 1
            if cautious:
                break
    return current == (n-1, n-1), entered, moves

def main():
    print("TASK 6: RESCUE GRID AGENT")
    for n in (4, 6, 8):
        success = hazards = moves = 0
        trials = 20
        for seed in range(trials):
            ok, hit, steps = run_agent(n, seed, True)
            success += int(ok); hazards += hit; moves += steps
        print(f"Grid {n}x{n}: success={success}/{trials} ({success/trials:.0%}); hazards entered={hazards}; average moves={moves/trials:.2f}")
    print("Policy: move to a provably safe unvisited neighbour; if none exists, choose the least-risk unvisited neighbour.")
    print("Limitation: the demonstration uses a conservative hazard model; partial observability can still cause failure.")

if __name__ == "__main__":
    main()
