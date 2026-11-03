
male(ram).
male(surya).
male(kumar).

female(priya).
female(latha).

parent(ram, surya).
parent(latha, surya).
parent(ram, priya).
parent(latha, priya).
parent(surya, kumar).

father(X, Y) :-
    male(X),
    parent(X, Y).

mother(X, Y) :-
    female(X),
    parent(X, Y).

grandparent(X, Z) :-
    parent(X, Y),
    parent(Y, Z).

sibling(X, Y) :-
    parent(Z, X),
    parent(Z, Y),
    X \= Y.
