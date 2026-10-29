
parent(ram, surya).
parent(surya, kumar).

grandparent(X, Z) :-
    parent(X, Y),
    parent(Y, Z).
