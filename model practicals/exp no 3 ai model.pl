
eligible(M, P, E) :-
    M >= 50,
    P >= 50,
    E >= 50.

check :-
    write('Enter Mathematics marks: '),
    read_line_to_string(user_input, A),
    number_string(M, A),

    write('Enter Programming marks: '),
    read_line_to_string(user_input, B),
    number_string(P, B),

    write('Enter English marks: '),
    read_line_to_string(user_input, C),
    number_string(E, C),

    (eligible(M, P, E) ->
        write('Student is Eligible')
    ;
        write('Student is Not Eligible')
    ).
