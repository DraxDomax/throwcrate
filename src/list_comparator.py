"""
The following requires knowledge of the mathematical field of "List Theory" - which you will not have, as I've
just invented it!

List Theory: The study of unsorted groups that allow duplicates (because the hell with Set Theory...)
Here are some initial definitions:
- When two or more lists are compared, they exist on the same "level".
- Any element that appears on all lists at the level is called a "horizon".

Operators of list theory:
A.  Annihilation

    "{A, B, B, C} annihilate {A, B, D}"
    - Each operand (list) is called a "nihilant"
    - From all lists at the level, the shortest list is called the "key nihilant"
    Result: {B, C} and {D}
    (All horizons are removed)

    To reiterate: Duplicates in a list are not removed, unless there's a horizon to annihilate them:
    {B, B, B} annihilate {B, B}
    Result: {B} and {}

    1.  First law of Annihilation:
        "The maximum number of horizons is equal to the number of members of the key nihilant" (Nobel prize in
        mathematics if you prove it! 😃 )

/* I ported this from my work in Java. I did not like any of the Collections available, nor am I a fan of streaming
relatively small objects. I am pretty sure Python has something more suitable but I resorted to what I know */
"""


def annihilate(list_a, list_b):
    working_list_a = list_a.copy()
    working_list_b = list_b.copy()

    key_nihilant = working_list_a
    other_nihilant = working_list_b

    if len(working_list_a) > len(working_list_b):
        key_nihilant = working_list_b
        other_nihilant = working_list_a

    reverse_index = len(key_nihilant) - 1
    while reverse_index > -1:
        foreign_index = find_first(other_nihilant, key_nihilant[reverse_index])
        if foreign_index != -1:
            other_nihilant.pop(foreign_index)
            key_nihilant.pop(reverse_index)
        reverse_index -= 1

    return working_list_a, working_list_b


def find_first(containing_list, query):
    for index in range(len(containing_list)):
        if containing_list[index] == query:
            return index
    return -1
