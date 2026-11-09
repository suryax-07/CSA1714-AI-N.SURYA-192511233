# Redesign of Task 4: memoize both successful and failed backward subgoals.
def backward(goal, facts, rules, memo=None, active=None, stats=None):
    memo = memo if memo is not None else {}
    active = active if active is not None else set()
    stats = stats if stats is not None else {"calls": 0, "rule_checks": 0, "memo_hits": 0}
    stats["calls"] += 1
    if goal in facts:
        return True
    if goal in memo:
        stats["memo_hits"] += 1
        return memo[goal]
    if goal in active:
        return False
    active.add(goal)
    answer = False
    for premises, conclusion in rules:
        stats["rule_checks"] += 1
        if conclusion == goal and all(backward(p, facts, rules, memo, active.copy(), stats) for p in premises):
            answer = True
            break
    active.remove(goal)
    memo[goal] = answer
    return answer

def main():
    rules = [
        (["sensor_alarm", "power_ok"], "router_fault"),
        (["router_fault"], "network_down"),
        (["dns_alarm"], "dns_fault"),
        (["dns_fault", "network_down"], "payroll_unreachable"),
        (["router_fault"], "ticket_required"),
        (["network_down"], "incident_open"),
        (["missing_fact"], "unknown_diagnosis")
    ]
    facts = {"sensor_alarm", "power_ok", "dns_alarm"}
    goals = ["payroll_unreachable", "ticket_required", "incident_open", "unknown_diagnosis",
             "payroll_unreachable", "ticket_required", "unknown_diagnosis"]
    # Original baseline: no cross-query memo table; each query starts fresh.
    base_total = {"calls": 0, "rule_checks": 0}
    for g in goals:
        st = {"calls": 0, "rule_checks": 0, "memo_hits": 0}
        backward(g, facts, rules, memo={}, stats=st)
        base_total["calls"] += st["calls"]
        base_total["rule_checks"] += st["rule_checks"]
    # Redesigned: share successful and failed subgoal results across queries.
    shared_memo = {}
    new_total = {"calls": 0, "rule_checks": 0, "memo_hits": 0}
    results = []
    for g in goals:
        st = {"calls": 0, "rule_checks": 0, "memo_hits": 0}
        result = backward(g, facts, rules, memo=shared_memo, stats=st)
        results.append(result)
        for k in new_total:
            new_total[k] += st[k]
    print("TASK 7: REDESIGN VALIDATION")
    print("Queries:", goals)
    print("Answers:", results)
    print(f"Original no cross-query cache: calls={base_total['calls']}; rule checks={base_total['rule_checks']}")
    print(f"Redesigned shared cache: calls={new_total['calls']}; rule checks={new_total['rule_checks']}; memo hits={new_total['memo_hits']}")
    if base_total["rule_checks"]:
        improvement = (1 - new_total["rule_checks"] / base_total["rule_checks"]) * 100
    else:
        improvement = 0
    print(f"Rule-check reduction: {improvement:.1f}%")
    print("Trade-off: memory is used to store answers; the cache must be cleared when facts/rules change.")

if __name__ == "__main__":
    main()
