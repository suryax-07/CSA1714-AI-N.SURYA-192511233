# Terms are represented as strings (variables start with uppercase) or tuples:
# ("function_name", argument1, argument2, ...)
def is_var(x):
    return isinstance(x, str) and x[:1].isupper()

def walk(x, subst):
    while is_var(x) and x in subst:
        x = subst[x]
    return x

def occurs(v, term, subst):
    term = walk(term, subst)
    if v == term:
        return True
    if isinstance(term, tuple):
        return any(occurs(v, t, subst) for t in term[1:])
    return False

def unify(x, y, subst=None):
    subst = dict(subst or {})
    x, y = walk(x, subst), walk(y, subst)
    if x == y:
        return subst
    if is_var(x):
        if occurs(x, y, subst):
            return None
        subst[x] = y
        return subst
    if is_var(y):
        if occurs(y, x, subst):
            return None
        subst[y] = x
        return subst
    if isinstance(x, tuple) and isinstance(y, tuple) and x[0] == y[0] and len(x) == len(y):
        for a, b in zip(x[1:], y[1:]):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    return None

def show(value):
    return "FAIL" if value is None else str(value)

def cnf_demo():
    # Illustrative standard transformations for quantified examples.
    examples = [
        ("forall x exists y Likes(x,y)", "Likes(x, f(x))"),
        ("exists y forall x Helps(y,x)", "Helps(c, x)"),
        ("forall x (Human(x) -> Mortal(x))", "~Human(x) OR Mortal(x)"),
        ("forall x (P(x) AND Q(x))", "P(x) AND Q(x)"),
        ("exists x (Student(x) AND Smart(x))", "Student(sk1) AND Smart(sk1)")
    ]
    print("CLAUSE-FORM CONVERSION EXAMPLES")
    for source, result in examples:
        print(source, "=>", result)

def main():
    tests = [
        ("X", "alice"), ("X", "Y"), (("f", "X"), ("f", "bob")),
        (("f", "X", "X"), ("f", "alice", "alice")),
        (("f", "X", "X"), ("f", "alice", "bob")),
        (("g", ("f", "X")), ("g", ("f", "carol"))),
        (("f", "X"), ("g", "X")), ("alice", "bob"),
        ("X", ("f", "X")), (("f", "X", "Y"), ("f", "a", "b")),
        (("h", ("g", "X")), ("h", ("g", "d"))),
        (("f", "X", "Y"), ("f", "Y", "a"))
    ]
    print("TASK 3: UNIFICATION TESTS")
    for i, (a, b) in enumerate(tests, 1):
        print(f"{i}. {a} with {b} => {show(unify(a,b))}")
    cnf_demo()
    print("MGU is most general because it imposes only substitutions required for the terms to match.")
    print("Occurs check prevents cyclic substitutions such as X=f(X).")

if __name__ == "__main__":
    main()
