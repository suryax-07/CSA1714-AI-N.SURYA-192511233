
RULES = [
    ({"low_flow","high_pressure"}, "blocked_pipe", 3),
    ({"low_flow","pump_noise"}, "bearing_wear", 2),
    ({"motor_hot","high_current"}, "motor_overload", 3),
    ({"leak","low_pressure"}, "pipe_leak", 3),
    ({"vibration","pump_noise"}, "bearing_wear", 2),
    ({"no_start","no_power"}, "electrical_failure", 4),
    ({"no_start","high_current"}, "motor_overload", 3),
    ({"low_flow","filter_dirty"}, "blocked_pipe", 2),
    ({"water_loss","low_pressure"}, "pipe_leak", 2),
    ({"motor_hot","vibration"}, "motor_overload", 2),
    ({"fuse_blown","no_power"}, "electrical_failure", 4),
    ({"shaft_noise","vibration"}, "bearing_wear", 3),
    ({"high_pressure","filter_dirty"}, "blocked_pipe", 2),
    ({"cable_damage","no_start"}, "electrical_failure", 3),
    ({"leak","water_loss"}, "pipe_leak", 3)
]

def diagnose(facts, strategy="specificity"):
    matched = []

    for conditions, fault, priority in RULES:
        if conditions.issubset(facts):
            matched.append((conditions, fault, priority))

    if not matched:
        return "Unknown", []

    if strategy == "priority":
        matched.sort(key=lambda x: -x[2])
    else:
        matched.sort(key=lambda x: -len(x[0]))

    return matched[0][1], matched

def main():
    print("PUMP FAULT EXPERT SYSTEM")

    tests = [
        {"low_flow","high_pressure"},
        {"motor_hot","high_current"},
        {"leak","low_pressure"},
        {"no_start","no_power"},
        {"vibration","pump_noise"},
        {"fuse_blown","no_power"}
    ]

    for facts in tests:
        result, rules = diagnose(facts)

        print("\\nFacts:", facts)
        print("Diagnosis:", result)
        print("Rules fired:", len(rules))

    print("\\nADVERSARIAL TEST")

    facts = {"low_flow","high_pressure","pump_noise"}

    print("Facts:", facts)

    print("Specificity:", diagnose(facts, "specificity")[0])
    print("Priority:", diagnose(facts, "priority")[0])

    print("\\nKNOWLEDGE ACQUISITION")

    RULES.append(
        ({"seal_damaged"}, "pipe_leak", 5)
    )

    print("New rule added successfully")
    print("New diagnosis:", diagnose({"seal_damaged"})[0])

if __name__ == "__main__":
    main()
