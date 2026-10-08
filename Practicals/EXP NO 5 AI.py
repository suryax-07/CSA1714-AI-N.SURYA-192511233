from collections import deque

def safe(m, c):
    if m < 0 or c < 0 or m > 3 or c > 3:
        return False

    if m > 0 and m < c:
        return False

    if 3 - m > 0 and 3 - m < 3 - c:
        return False

    return True

def solve():
    start = (3, 3, 0)
    goal = (0, 0, 1)

    queue = deque([(start, [])])
    visited = {start}

    moves = [
        (1, 0), (2, 0),
        (0, 1), (0, 2),
        (1, 1)
    ]

    while queue:
        state, path = queue.popleft()
        m, c, boat = state

        if state == goal:
            for step in path:
                print(step)
            return

        for dm, dc in moves:
            if boat == 0:
                new_state = (m - dm, c - dc, 1)
                direction = "Right"
            else:
                new_state = (m + dm, c + dc, 0)
                direction = "Left"

            if safe(*new_state[:2]) and new_state not in visited:
                visited.add(new_state)
                step = (new_state, direction)
                queue.append((new_state, path + [step]))

solve()
