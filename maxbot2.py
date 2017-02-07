from __future__ import division
from codefights.model.IFighter import *
import codefights.boilerplate.SDK
from collections import Counter
from random import uniform
import sys

################################
# Probabilities
################################

moves = set()
ms = (3, 4, 6, 8, 10)
for m1 in ms:
    for m2 in ms:
        for m3 in ms:
            moves.add(tuple(sorted((m1, m2, m3))))
for move in list(moves):
    for b in range(1, 8):
        t = list(move)
        for i in range(3):
            if (b // (2 ** i)) % 2:
                t[i] *= -1
        b = sorted(i for i in t if i < 0)
        if b == sorted(set(b)):
            moves.add(tuple(sorted(t)))
moves = sorted(moves)

n = len(moves)
top = [[0] * n for i in range(n)]
for i in range(n):
    for j in range(n):
        for m in moves[i]:
            if m > 0 and -m not in moves[j]:
                top[i][j] += m
top = [[top[i][j] - top[j][i] for j in range(n)] for i in range(n)]
top = [sorted((a[i], i) for i in range(len(a))) for a in top]
best_opp_moves = set(index for row in top for score, index in row[:5])

#moveSet = {3, 4, 5, 6, 7, 27, 28, 32, 36, 39, 65, 70, 72, 97, 98, 144, 147, 158, 160, 161, 162, 164}

moveSet = {5, 6, 7, 28, 32, 36, 39, 40, 65, 70, 71, 72, 73, 97, 98, 160, 161, 162, 163, 164, 165, 166, 167, 169} #99, 27, 169, 168, 32, 158, 40, 73, 99, 3, 4,  27, 28, 150, 158, 99, 163, 164, 166, 169}  #|best_opp_moves
# rem: 99, 27, 169, 168, 32, 158,
# doubles: 40, 73, 99
# weaks: 3, 4,  27, 28, 150, 158,99
# strongs: 163, 164, 166, 169

"""
3(-10, -8, 3)
4(-10, -8, 4)
5(-10, -8, 6)
6(-10, -8, 8)
7(-10, -8, 10)
27(-10, 4, 3)
28(-10, 6, 3)
32(-10, 6, 4)
39(-10, 8, 10)
40(-10, 10, 10)!
64(-8, 4, 4)!
68(-8, 6, 6)!
70(-8, 6, 10)
71(-8, 8, 8)!
72(-8, 8, 10)
73(-8, 10, 10)!
99(-6, 10, 10)!
150(4, 4, 4)
158(4, 8, 10)
160(6, 6, 6)
161(6, 6, 8)
162(6, 6, 10)
163(6, 8, 8)
164(6, 8, 10)
165(6, 10, 10)!
166(8, 8, 8)!
167(8, 8, 10)!
168(8, 10, 10)!

"""

moveToIndex = lambda m1, m2, m3: moves.index(tuple(sorted((m1, m2, m3))))
bestMove = lambda m1, m2, m3: moves[top[moveToIndex(m1, m2, m3)][0][1]]


#####################
# Predictions
#####################

def predict_next(sequence):
    # type: (List[List[int]]) -> Tuple[int, int, int]
    last_elem = sequence[-1]
    all_indices = [i for i, x in enumerate(sequence[:-1]) if x == last_elem]

    all_predictions = [tuple(sequence[index + 1]) for index in all_indices]
    c = Counter(all_predictions)
    if len(c.items()) == 1:
        return all_predictions[0]
    elif len(c.items()) == 0:
        return None
    else:
        best_attack, best_chance = c.most_common(1)[0]
        if uniform(0, 1) < best_chance / len(all_predictions) > 0.95 and best_chance >= 2:
            return best_attack
        else:
            return None


######################
# Bot utilities
#####################

def weighted_choice(items):
    # type: (List[Tuple[int, float]]) -> int
    choices = []
    for x, y in items:
        if y > 0:
            choices.append((x, y*y*0.15))
        else:
            choices.append((x, 0.1))

    total = sum(x for name, x in choices)
    r = uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


move_points = {
    "NOSE": 10,
    "JAW": 8,
    "BELLY": 6,
    "GROIN": 4,
    "LEGS": 3,
    "ATTACK": 1,
    "BLOCK": -1
}

point_moves = {v: k for k, v in move_points.iteritems()}


def str_to_index(s):
    # type: (str) -> int
    s = s.split()[1: 7]
    s = [move_points[word] for word in s]
    s = tuple((s[2 * i] * s[2 * i + 1]) for i in range(3))
    return moves.index(tuple(sorted(s)))


#######################
# Bot class
#######################

class Fighter(IFighter):
    def __init__(self):
        self.my_hp = 150
        self.opp_hp = 150
        self.turn_number = 0
        self.opp_moves = []

        self.W = {i: 0 for i in moveSet}
        for i in best_opp_moves:  # range(170):
            self.change_weights(i, reaction=0.08)

    def change_weights(self, move, reaction=1):
        # type: (int, float) -> None
        for score, index in top[move]:
            if index in self.W:
                self.W[index] -= score * reaction

    def make_next_move(self,
                       opponents_last_move,
                       my_last_score=0,
                       opponents_last_score=0):
        # type: (Union[None, codefights.model.Move.Move], int, int) -> codefights.model.Move.Move

        if opponents_last_move is not None:
            self.analyze(opponents_last_move)

        if self.turn_number > 4:
            try:
                predicted_move = predict_next(self.opp_moves)
                if predicted_move:
                    counter = bestMove(*predicted_move)
                    counter_move = Move()
                    for points in counter:
                        if points > 0:
                            counter_move.add_attack(point_moves[points])
                        else:
                            counter_move.add_block(point_moves[-points])
                    #assert len(counter_move.attacks) + len(counter_move.blocks) == 3, "Full move"
                    return counter_move
            except Exception as e:
                #print(e)
                pass

        return self.weighted_choice_move()

    def analyze(self, opp_move):
        # type: (codefights.model.Move.Move) -> None
        try:
            self.change_weights(str_to_index(repr(opp_move)), reaction=5)
        except Exception as e:
            #print(e)
            pass
        # Degrade
        for i in self.W:
            self.W[i] = self.W[i] - 3

        self.opp_moves.append(sorted(map(lambda x: move_points[x], opp_move.attacks) +
                                     map(lambda x: -move_points[x], opp_move.blocks)))

        self.turn_number += 1

    def weighted_choice_move(self):
        # type: () -> codefights.model.Move.Move
        choice = weighted_choice(self.W.items())
        choice = moves[choice]
        good_move = Move()
        for points in choice:
            if points > 0:
                good_move.add_attack(point_moves[points])
            else:
                good_move.add_block(point_moves[-points])

        #assert len(good_move.attacks) + len(good_move.blocks) == 3, "Full move"
        return good_move


##################
# Arguments
##################


if __name__ == '__main__':
    codefights.boilerplate.SDK.SDK.run(Fighter, sys.argv)
    # codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-me"])
    # codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-on-server"])

    """
    print("Laura++:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "laura++"])
    print("Jess:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "jess"])
    print("Datahost:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "datahost"])

    #
    print("Kickboxer:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "kickboxer"])
    print("Boxer:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "boxer"])
    print("Laura:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "laura"])
    print("PeeGrabber:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "peegrabber"])
    print("StupidBot:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "stupidbot"])
    """
