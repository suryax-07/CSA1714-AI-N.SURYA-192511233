
sum(0, 0).

sum(N, S) :-
    N > 0,
    N1 is N - 1,
    sum(N1, S1),
    S is N + S1.
sum(5, S).
sum(5, S).

consult('c:/users/surya/downloads/EXP NO 16 AI.pl').

