
bird(parrot).
bird(pigeon).
bird(sparrow).
bird(ostrich).
bird(penguin).

can_fly(X) :-
    bird(X),
    X \= ostrich,
    X \= penguin.

cannot_fly(ostrich).
cannot_fly(penguin).
