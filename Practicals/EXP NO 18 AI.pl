% Facts: teaches(Teacher, SubjectCode)
teaches(mr_smith, cs101).
teaches(ms_davis, cs102).
teaches(dr_jones, math201).

% Facts: student_enrolled(Student, SubjectCode)
student_enrolled(alice, cs101).
student_enrolled(bob, cs101).
student_enrolled(charlie, cs102).
student_enrolled(diana, math201).

% Rule: A teacher teaches a student if the teacher teaches a subject code and the student is enrolled in that subject code
teacher_of(Teacher, Student) :-
    teaches(Teacher, SubjectCode),
    student_enrolled(Student, SubjectCode).

% Rule: Find the subject code a student is taking and who teaches it
student_info(Student, SubjectCode, Teacher) :-
    student_enrolled(Student, SubjectCode),
    teaches(Teacher, SubjectCode).
