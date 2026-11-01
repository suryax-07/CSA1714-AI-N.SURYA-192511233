
hanoi(1, A, _, C) :-
    write('Move disk from '),
    write(A),
    write(' to '),
    write(C),
    nl.

hanoi(N, A, B, C) :-
    N > 1,
    M is N - 1,
    hanoi(M, A, C, B),
    hanoi(1, A, B, C),
    hanoi(M, B, A, C).
