
initial_state(at(door), on_floor, at(window), has_not).

move(state(at(X), on_floor, B, H),
     state(at(Y), on_floor, B, H)) :-
    X \= Y.

push_box(state(at(X), on_floor, at(X), H),
         state(at(Y), on_floor, at(Y), H)) :-
    X \= Y.

climb(state(at(X), on_floor, at(X), H),
      state(at(X), on_box, at(X), H)).

grasp(state(at(middle), on_box, at(middle), has_not),
      state(at(middle), on_box, at(middle), has)).

can_get_banana :-
    initial_state(S),
    move(S, S1),
    push_box(S1, S2),
    climb(S2, S3),
    grasp(S3, S4),
    write(S4).
