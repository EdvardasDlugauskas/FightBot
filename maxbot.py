from __future__ import division
from codefights.model.IFighter import *
import codefights.boilerplate.SDK
from collections import Counter
import sys

move_points = {
        "NOSE": 10,
        "JAW": 8,
        "BELLY": 6,
        "GROIN": 4,
        "LEGS": 3
    }

point_moves = {v: k for k, v in move_points}


def predict_next(sequence):
    try:
        last_elem = sequence[-1]
        all_indices = [i for i, x in enumerate(sequence[:-1]) if x == last_elem]

        c = Counter([sequence[index + 1] for index in all_indices])
        return c.items()
    except Exception as e:
        print("Exception in predict_next():" + str(e))
        return ()


def predict_next_move(opp_sequence):
    prediction = predict_next(opp_sequence)
    if len(prediction) == 1:
        predicted_attack = set(prediction[0][0])
        try:
            return max(predicted_attack, key=lambda x: move_points[x])
        except:
            return None
    return None


class Fighter(IFighter):
    def __init__(self):
        self.my_hp = 150
        self.opp_hp = 150
        self.turn_number = 0
        self.opp_attacks = []
        self.opp_blocks = []

    def make_next_move(self,
                       opponents_last_move,
                       my_last_score=0,
                       opponents_last_score=0):
        try:
            # Analyze and record
            self.turn_number += 1
            if my_last_score is not None and opponents_last_score is not None:
                self.my_hp -= opponents_last_score
                self.opp_hp -= my_last_score

            if opponents_last_move is not None:
                self.opp_attacks.append(tuple(opponents_last_move.attacks))
                self.opp_blocks.append(tuple(opponents_last_move.blocks))

            # Make move
            move = Move()
            if self.turn_number > 4:
                predicted_attack = predict_next_move(self.opp_attacks)
                predicted_block = predict_next_move(self.opp_blocks)

                if self.my_hp/self.opp_hp > 1.0:
                    for att in ["NOSE", "JAW", "BELLY", "GROIN", "LEGS"]:
                        if att != predicted_block and len(move.attacks) < 3:
                            move.add_attack(att)
                    return move
                else:
                    if predicted_attack is not None:
                        move.add_block(predicted_attack)
                    else:
                        move.add_block("NOSE")

                    for att in ["JAW", "BELLY", "GROIN", "LEGS"]:
                        if att != predicted_block and len(move.attacks) < 2:
                            move.add_attack(att)
                    return move
            else:
                move.add_block("NOSE").add_attack("JAW").add_attack("BELLY")
                return move
        except Exception as e:
            print("Something horrible happened:" + str(e))
            return Move().add_block("NOSE").add_attack("JAW").add_attack("BELLY")


if __name__ == '__main__':
    codefights.boilerplate.SDK.SDK.run(Fighter, sys.argv)
    #codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-me"])
    #codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-on-server"])


    print("Kickboxer:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "kickboxer"])
    print("Boxer:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "boxer"])
    print("Laura++:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "laura++"])
    print("PeeGrabber:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "peegrabber"])

