sequence1 = "ABCABCABDABCAB"
from collections import Counter

def predict_next(sequence):
    assert len(sequence) > 2, "Length should be more than 2"
    last_elem = sequence[-1]
    all_indices = [i for i, x in enumerate(sequence[:-1]) if x == last_elem]

    c = Counter([sequence[index + 1] for index in all_indices])
    return c.items()

print(predict_next(sequence1))

def parse_move(move_str):
    move = Move()
    for my_move in move_str.split(" "):
        if my_move.lower()[0] == "a":
            func = move.add_attack
        else:
            func = move.add_block

        area = dict(n="NOSE", j="JAW", b="BELLY", g="GROIN", l="LEGS")[my_move[1].lower()]

        func(area)
    return move