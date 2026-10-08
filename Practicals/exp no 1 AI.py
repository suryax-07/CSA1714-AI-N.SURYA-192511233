from collections import deque

start = (1, 2, 3,
         4, 0, 6,
         7, 5, 8)

goal = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

queue = deque()
queue.append((start, []))

visited = set()
visited.add(start)

while queue:

    state, path = queue.popleft()

    if state == goal:
        print("Solution found!")

        for step in path + [state]:
            print(step[0], step[1], step[2])
            print(step[3], step[4], step[5])
            print(step[6], step[7], step[8])
            print()
        break

    zero = state.index(0)

    row = zero // 3
    col = zero % 3

    moves = [-3, 3, -1, 1]

    for move in moves:

        new = zero + move

        if new < 0 or new >= 9:
            continue

        if move == -1 and col == 0:
            continue

        if move == 1 and col == 2:
            continue

        new_state = list(state)

        new_state[zero] = new_state[new]
        new_state[new] = 0

        new_state = tuple(new_state)

        if new_state not in visited:

            visited.add(new_state)

            queue.append((new_state, path + [state]))
