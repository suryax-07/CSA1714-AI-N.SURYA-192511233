from itertools import product
import time

SYMBOLS = ["T", "B", "S", "E", "A", "V", "C", "D", "R", "O", "G", "L"]
# T=training, B=booking, S=supervisor approval, E=emergency override,
# A=access granted, V=safety test valid, C=clearance, D=door operational,
# R=restricted, O=security officer present, G=guest pass, L=lab open.

def kb(bits):
    T, B, S, E, A, V, C, D, R, O, G, L = [bits[x] for x in SYMBOLS]
    return [
        (not A) or (T and B and S and V and C and D),  # access requires conditions
        (not E) or A,                                  # emergency override grants access
        (not (T and B and S and V and C and D)) or A,
        (not V) or C,
        (not R) or (not A),
        (not O) or D,
        (not G) or (B and S),
        (not L) or D,
        (not (T and V)) or C,
        (not (E and R)) or (not A),                   # conflict with override if restricted
        (not (T and B and S and V and C and D)) or A # duplicate support rule
    ]

def entails(query, fixed=None):
    fixed = fixed or {}
    checked = 0
    for values in product([False, True], repeat=len(SYMBOLS)):
        model = dict(zip(SYMBOLS, values))
        if any(model[k] != v for k, v in fixed.items()):
            continue
        checked += 1
        if all(kb(model)) and not query(model):
            return False, checked
    return True, checked

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
    return known, firings

def main():
    print("TASK 1: PROPOSITIONAL LOGIC")
    # Demonstration queries over the full 12-symbol KB.
    t0 = time.perf_counter()
    q1, m1 = entails(lambda m: m["A"], {"T": True, "B": True, "S": True, "V": True, "C": True, "D": True})
    q2, m2 = entails(lambda m: m["A"], {"T": False, "B": False, "S": False, "V": False, "C": False, "D": False, "E": False})
    # Inconsistent restriction: A and R are both required, while KB says R -> not A.
    q3, m3 = entails(lambda m: m["A"], {"A": True, "R": True})
    elapsed = time.perf_counter() - t0
    print(f"Query 1 (valid access conditions imply access): {q1}; models examined={m1}")
    print(f"Query 2 (no conditions, no override): {q2}; models examined={m2}")
    print(f"Query 3 (inconsistent A and restricted): {q3}; models examined={m3}")
    print(f"Elapsed seconds for three checks: {elapsed:.6f}")
    facts = {"TRAINED", "BOOKED", "APPROVED", "TEST_VALID", "CLEAR", "DOOR_OK"}
    rules = [
        (["TRAINED", "BOOKED", "APPROVED", "TEST_VALID", "CLEAR", "DOOR_OK"], "ACCESS"),
        (["EMERGENCY"], "ACCESS"),
        (["TEST_VALID"], "CLEAR")
    ]
    derived, firings = forward_chain(facts, rules)
    print(f"Forward chaining derives ACCESS: {'ACCESS' in derived}; rule firings={firings}")
    print("Prediction: a full truth table checks 2^n assignments; at n=12 this is 4096 assignments.")
    for n in (8, 12, 16, 20):
        print(f"n={n}: possible assignments={2**n}")

if __name__ == "__main__":
    main()
