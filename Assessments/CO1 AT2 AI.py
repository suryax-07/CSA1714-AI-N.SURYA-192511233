variables = ['A', 'B', 'C', 'D', 'E']

domains = {
    'A': ['Slot1', 'Slot2', 'Slot3'],
    'B': ['Slot1', 'Slot2', 'Slot3'],
    'C': ['Slot1', 'Slot2', 'Slot3'],
    'D': ['Slot1', 'Slot2', 'Slot3'],
    'E': ['Slot1', 'Slot2', 'Slot3']
}

neighbors = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D', 'E'],
    'D': ['B', 'C', 'E'],
    'E': ['C', 'D']
}

def is_valid(variable, value, assignment):
    for neighbor in neighbors[variable]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True


attempts_bt = 0
backtracks_bt = 0

def backtracking(assignment):
    global attempts_bt, backtracks_bt

    if len(assignment) == len(variables):
        return assignment.copy()

    variable = variables[len(assignment)]

    for value in domains[variable]:
        attempts_bt += 1

        if is_valid(variable, value, assignment):
            assignment[variable] = value

            result = backtracking(assignment)

            if result is not None:
                return result

            del assignment[variable]
            backtracks_bt += 1

    return None


attempts_fc = 0
backtracks_fc = 0

def forward_checking(assignment, current_domains):
    global attempts_fc, backtracks_fc

    if len(assignment) == len(variables):
        return assignment.copy()

    variable = variables[len(assignment)]

    for value in current_domains[variable]:
        attempts_fc += 1

        if is_valid(variable, value, assignment):
            new_assignment = assignment.copy()
            new_assignment[variable] = value

            new_domains = {
                var: current_domains[var].copy()
                for var in variables
            }

            failed = False

            for neighbor in neighbors[variable]:
                if neighbor not in new_assignment:
                    if value in new_domains[neighbor]:
                        new_domains[neighbor].remove(value)

                    if len(new_domains[neighbor]) == 0:
                        failed = True
                        break

            if not failed:
                result = forward_checking(
                    new_assignment,
                    new_domains
                )

                if result is not None:
                    return result

            backtracks_fc += 1

    return None


plain_result = backtracking({})

forward_result = forward_checking(
    {},
    {var: domains[var].copy() for var in variables}
)

print("Plain Backtracking Result:")
print(plain_result)
print("Assignment Attempts:", attempts_bt)
print("Backtracks:", backtracks_bt)

print()

print("Forward Checking Result:")
print(forward_result)
print("Assignment Attempts:", attempts_fc)
print("Backtracks:", backtracks_fc)
