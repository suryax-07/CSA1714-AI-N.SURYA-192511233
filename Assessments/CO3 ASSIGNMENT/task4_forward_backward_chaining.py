from collections import defaultdict

def forward_chain(facts, rules):
    known = set(facts)
    firings = 0
    changed = True
    while changed:
        changed = False
        for premises, conclusion in rules:
            if set(premises).issubset(known) and conclusion not in known:
                known.add(conclusion)
                firings += 1
                changed = True
    return conclusion in known, known, firings

def backward_chain(goal, facts, rules, active=None, memo=None, stats=None):
    active = active or set()
    memo = memo if memo is not None else {}
    stats = stats if stats is not None else {"subgoals": 0, "repeats": 0, "rule_checks": 0}
    stats["subgoals"] += 1
    if goal in facts:
        return True
    if goal in memo:
        stats["repeats"] += 1
        return memo[goal]
    if goal in active:
        stats["repeats"] += 1
        return False
    active.add(goal)
    answer = False
    for premises, conclusion in rules:
        stats["rule_checks"] += 1
        if conclusion == goal and all(backward_chain(p, facts, rules, active.copy(), memo, stats) for p in premises):
            answer = True
            break
    active.remove(goal)
    memo[goal] = answer
    return answer

def make_rules(count=30):
    rules = [
        (["router_alarm", "router_power"], "router_fault"),
        (["router_fault"], "network_down"),
        (["dns_alarm"], "dns_fault"),
        (["dns_fault", "network_down"], "payroll_unreachable"),
        (["switch_alarm"], "switch_fault"),
        (["switch_fault"], "network_down"),
    ]
    for i in range(24):
        rules.append(([f"unused_fact_{i}"], f"unused_result_{i}"))
    return rules[:count]

def main():
    print("TASK 4: FORWARD AND BACKWARD CHAINING")
    rules = make_rules(30)
    facts = {"router_alarm", "router_power", "dns_alarm"}
    goal = "payroll_unreachable"
    ok, derived, firings = forward_chain(facts, rules)
    stats = {"subgoals": 0, "repeats": 0, "rule_checks": 0}
    back = backward_chain(goal, facts, rules, stats=stats)
    print(f"Forward: proved={ok}; rule firings={firings}; derived facts={len(derived)}")
    print(f"Backward: proved={back}; subgoals={stats['subgoals']}; repeated={stats['repeats']}; rule checks={stats['rule_checks']}")
    cyclic = [(["a"], "b"), (["b"], "a"), (["b"], "goal")]
    cycle_stats = {"subgoals": 0, "repeats": 0, "rule_checks": 0}
    cycle_result = backward_chain("goal", set(), cyclic, stats=cycle_stats)
    print(f"Cyclic KB: proved={cycle_result}; subgoals={cycle_stats['subgoals']}; repeated/cycle detections={cycle_stats['repeats']}")
    print("Prediction: backward chaining focuses on one requested goal; forward chaining is useful when many consequences are needed.")

if __name__ == "__main__":
    main()
