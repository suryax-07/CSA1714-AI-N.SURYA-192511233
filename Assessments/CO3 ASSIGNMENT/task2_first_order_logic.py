# Course registration advisory system using Python rules.
courses = {"PY101", "DS201", "AI301", "DB202"}
students = {"surya"}
passed = {("surya", "PY101"), ("surya", "DB202")}
prereq = {("DS201", "PY101"), ("AI301", "DS201")}  # (course, required course)
credits = {"PY101": 3, "DS201": 4, "AI301": 4, "DB202": 3}
timetable = {"DS201": "MON10", "AI301": "TUE10", "DB202": "MON10", "PY101": "WED10"}
programme_allowed = {("surya", c) for c in courses}
credit_limit = {"surya": 18}
current_credits = {"surya": 9}
offered = courses.copy()

def prerequisite_closure(course):
    required = set()
    stack = [course]
    while stack:
        current = stack.pop()
        for c, p in prereq:
            if c == current and p not in required:
                required.add(p)
                stack.append(p)
    return required

def eligible(student, course):
    reasons = []
    if course not in courses or course not in offered:
        reasons.append("course not offered or unknown")
        return False, reasons
    if (student, course) not in programme_allowed:
        reasons.append("programme restriction")
    missing = prerequisite_closure(course) - {c for s, c in passed if s == student}
    if missing:
        reasons.append("missing prerequisites: " + ", ".join(sorted(missing)))
    if current_credits.get(student, 0) + credits[course] > credit_limit.get(student, 0):
        reasons.append("credit limit exceeded")
    for (s, existing), _ in [(x, None) for x in []]:
        pass
    # Current registration example: DB202; same slot means clash.
    registered = {"surya": {"DB202"}}
    if any(timetable.get(x) == timetable.get(course) for x in registered.get(student, set())):
        reasons.append("timetable clash")
    return len(reasons) == 0, reasons

def flawed_universal_conjunction(student, course):
    # Incorrectly treats all courses as prerequisites of every course.
    return all((student, p) in passed for p in courses if p != course)

def flawed_missing_transitive(student, course):
    # Incorrect: checks only direct prerequisites, not prerequisites of prerequisites.
    direct = {p for c, p in prereq if c == course}
    return direct.issubset({c for s, c in passed if s == student})

def main():
    print("TASK 2: FIRST-ORDER KNOWLEDGE ENGINEERING")
    queries = [
        ("surya", "DS201"), ("surya", "AI301"), ("surya", "DB202"),
        ("surya", "PY101"), ("surya", "UNKNOWN"), ("surya", "AI301"),
        ("guest", "DS201"), ("surya", "DB202")
    ]
    for s, c in queries:
        ok, why = eligible(s, c)
        print(f"Can {s} register {c}? {ok} | {', '.join(why) if why else 'all rules satisfied'}")
    print("Flaw 1 (universal conjunction) for DS201:", flawed_universal_conjunction("surya", "DS201"))
    print("Flaw 2 (missing transitive prerequisite) for AI301:", flawed_missing_transitive("surya", "AI301"))
    print("Repaired transitive check for AI301:", prerequisite_closure("AI301"))
    print("Vocabulary alternative A: Prereq(course, required_course) uses a compact binary relation.")
    print("Vocabulary alternative B: Requirement(course, requirement_object) is extensible but needs extra facts/rules.")

if __name__ == "__main__":
    main()
