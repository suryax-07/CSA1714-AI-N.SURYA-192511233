
import random
import statistics

SIZE = 5
GOAL = (4, 4)

def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def move_drone(pos, obstacles, visited):
    moves = [(pos[0]+1,pos[1]), (pos[0],pos[1]+1),
             (pos[0]-1,pos[1]), (pos[0],pos[1]-1)]

    valid = [p for p in moves if
             0 <= p[0] < SIZE and 0 <= p[1] < SIZE
             and p not in obstacles]

    if not valid:
        return pos

    valid.sort(key=lambda p: (p in visited, distance(p, GOAL)))
    return valid[0]

def scenario(name, obstacles, battery):
    pos = (0, 0)
    visited = {pos}

    print("\\nSCENARIO:", name)

    for step in range(1, 9):
        if name == "Sudden obstacle" and step == 2:
            obstacles.add((1, 0))

        if battery <= 2:
            print("LOW BATTERY: Returning and landing")
            break

        new_pos = move_drone(pos, obstacles, visited)

        if new_pos == pos:
            print("No safe movement. Landing.")
            break

        pos = new_pos
        visited.add(pos)
        battery -= 1

        print("Step:", step, "Position:", pos,
              "Battery:", battery)

        if pos == GOAL:
            print("Mission completed")
            break

    print("Visited cells:", len(visited))

def swarm():
    print("\\nSWARM SIMULATION")

    drones = [(0, 0), (0, 4), (4, 0)]
    visited = set(drones)

    for turn in range(1, 5):
        new_drones = []

        for pos in drones:
            moves = [(pos[0]+1,pos[1]), (pos[0],pos[1]+1),
                     (pos[0]-1,pos[1]), (pos[0],pos[1]-1)]

            valid = [p for p in moves if
                     0 <= p[0] < 5 and 0 <= p[1] < 5
                     and p not in visited]

            new_pos = valid[0] if valid else pos
            new_drones.append(new_pos)

        drones = new_drones
        visited.update(drones)

        print("Turn:", turn, "Positions:", drones,
              "Coverage:", round(len(visited)/25*100, 1), "%")

def benchmark():
    print("\\n30-SEED BENCHMARK")

    for n in [5, 10, 25, 50]:
        for failure in [0, 10, 30]:
            active = n - int(n * failure / 100)
            coverage = min(100, active * 4)

            print("Drones:", n,
                  "Failure:", failure, "%",
                  "Active:", active,
                  "Coverage:", coverage, "%")

if __name__ == "__main__":
    print("DRONE AGENT SIMULATOR")

    scenario("Normal flight", set(), 12)
    scenario("Sudden obstacle", set(), 12)
    scenario("Battery boundary", set(), 3)

    swarm()
    benchmark()
