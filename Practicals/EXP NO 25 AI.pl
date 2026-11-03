
disease(diabetes).
disease(anemia).
disease(obesity).

diet(diabetes, vegetables).
diet(diabetes, whole_grains).

diet(anemia, spinach).
diet(anemia, lentils).

diet(obesity, fruits).
diet(obesity, vegetables).

suggest_diet(Disease, Food) :-
    disease(Disease),
    diet(Disease, Food).
