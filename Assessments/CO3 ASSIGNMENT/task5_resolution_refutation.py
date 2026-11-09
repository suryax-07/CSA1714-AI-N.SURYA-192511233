from itertools import combinations

def canon(clause):
    return frozenset(clause)

def resolve(c1, c2):
    out = []
    for lit in c1:
        opposite = lit[1:] if lit.startswith("~") else "~" + lit
        if opposite in c2:
            merged = (set(c1) - {lit}) | (set(c2) - {opposite})
            if any((x[1:] if x.startswith("~") else "~"+x) in merged for x in merged):
                continue
            out.append(frozenset(merged))
    return out

def resolution(kb, strategy="all", limit=500):
    clauses = set(map(canon, kb))
    generated = 0
    steps = 0
    while steps < limit:
        pairs = list(combinations(sorted(clauses, key=lambda x: (len(x), sorted(x))), 2))
        if strategy == "unit":
            pairs.sort(key=lambda p: (0 if min(len(p[0]), len(p[1])) == 1 else 1, len(p[0])+len(p[1])))
        new = set()
        for a, b in pairs:
            steps += 1
            for r in resolve(a, b):
                if not r:
                    return True, generated, steps, len(clauses)
                if r not in clauses:
                    new.add(r)
                    generated += 1
            if steps >= limit:
                break
        if not new:
            return False, generated, steps, len(clauses)
        clauses |= new
    return False, generated, steps, len(clauses)

def main():
    print("TASK 5: RESOLUTION REFUTATION")
    # Puzzle: exactly one tamperer among five staff; encode facts/rules as clauses.
    # Unit facts and implications in clause form; query asks whether Alice tampered.
    kb = [
        {"T_A", "T_B", "T_C", "T_D", "T_E"},
        {"~T_A", "~T_B"}, {"~T_A", "~T_C"}, {"~T_A", "~T_D"}, {"~T_A", "~T_E"},
        {"~T_B", "~T_C"}, {"~T_B", "~T_D"}, {"~T_B", "~T_E"},
        {"~T_C", "~T_D"}, {"~T_C", "~T_E"}, {"~T_D", "~T_E"},
        {"~T_A", "ACCESS_A"}, {"~ACCESS_A", "T_A"}
    ]
    # Refute KB and not(T_A): append ~T_A.
    test_kb = kb + [{"~T_A"}]
    for strategy in ("all", "unit"):
        success, generated, steps, total = resolution(test_kb, strategy)
        print(f"Strategy={strategy}: empty_clause={success}; generated={generated}; resolution_steps={steps}; clauses={total}")
    # Non-entailed test: contradictory query assumption is absent; saturation stops.
    no_query = [{"P", "Q"}, {"~P", "Q"}]
    print("Non-entailed example:", resolution(no_query, "unit"))
    # FOL term growth illustration: p(X) -> p(f(X)); step-limited to show unbounded depth.
    term = "a"
    print("FOL function-symbol growth (bounded demonstration):")
    for i in range(6):
        print(f"step {i}: p({term})")
        term = f"f({term})"
    print("Without a step/depth limit, generated terms can grow indefinitely.")
    print("The empty clause means KB and the negated query are inconsistent; therefore KB entails the query.")

if __name__ == "__main__":
    main()
