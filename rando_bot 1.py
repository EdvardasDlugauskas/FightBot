from __future__ import division
from codefights.model.IFighter import *
import codefights.boilerplate.SDK
from random import uniform, choice
from collections import Counter
from sys import argv

BOT_REACTION_ADJ = 2
BOT_DEGRADATION = 1

attack_points = {
    "NOSE": 18,
    "JAW": 15,
    "BELLY": 10,
    "GROIN": 5,
    "LEGS": 4
}

block_points = {
    "NOSE": 18,
    "JAW": 15,
    "BELLY": 10,
    "GROIN": 5,
    "LEGS": 4
}

def predict_next(sequence):
    try:
        assert len(sequence) > 2, "Length should be more than 2"
        last_elem = sequence[-1]
        all_indices = [i for i, x in enumerate(sequence[:-1]) if x == last_elem]

        c = Counter([sequence[index + 1] for index in all_indices])
        return c.items()
    except:
        return ()


def probabilities(items):
    if len(items) == 0:
        return {}
    total = sum(items.values())
    try:
        return {k: v / total for k, v in items.iteritems()}
    except ZeroDivisionError:
        return {k: 1 / len(items) for k, v in items.iteritems()}


def weighted_choice(choices):
    choices = list(choices)
    total = sum(x for name, x in choices)
    r = uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def predict_next_move(opp_sequence):
    prediction = predict_next(opp_sequence)
    if len(prediction) == 1:
        predicted_attack = set(prediction[0][0])
        try:
            return max(predicted_attack, key=lambda x: block_points[x])
        except:
            return None
    return None


class Fighter(IFighter):


    opp_attack_pattern = {
        "NOSE": 10,
        "JAW": 8,
        "BELLY": 6,
        "GROIN": 4,
        "LEGS": 3
    }

    opp_block_pattern = {
        "NOSE": 10,
        "JAW": 8,
        "BELLY": 6,
        "GROIN": 4,
        "LEGS": 3
    }

    def __init__(self):
        self.turn_number = 1
        self.all_opp_attacks = []
        self.all_opp_blocks = []

    def create_move(self):
        move = Move()

        focused_areas = self.best_blocks()
        best_blocks_sorted = sorted(focused_areas, key=lambda x: x[1], reverse=True)
        block_amount = 0

        if 2 >= len(focused_areas) >= 1:
            block_amount = 1
            move.add_block(weighted_choice(best_blocks_sorted))
        elif len(focused_areas) == 2:
            block_amount = 2
            one, two = best_blocks_sorted
            move.add_block(one[0])
            move.add_block(two[0])
        elif len(focused_areas) == 0:
            block_amount = 0
        else:
            block_amount = 1
            move.add_block(weighted_choice(focused_areas))

        for i in range(3 - block_amount):
            move.add_attack(self.get_attack())

        assert len(move.blocks) == len(set(move.blocks))

        return move

    def get_attack(self):
        probs = probabilities(self.opp_block_pattern)
        scores = []
        for name, prob in probs.iteritems():
            scores.append((name, attack_points[name] * (1 - prob)))

        return weighted_choice(scores)

    def get_block(self):
        probs = probabilities(self.opp_attack_pattern)
        scores = []
        for name, prob in probs.iteritems():
            scores.append((name, block_points[name] * prob))

        return weighted_choice(scores)

    def best_blocks(self):
        probs = probabilities(self.opp_attack_pattern)
        scores = []
        for name, prob in probs.iteritems():
            scores.append((name, block_points[name] * prob))

        max_points = sum([x for y, x in scores])
        return [x for x in scores if x[1]/max_points > 0.33]

    def analyze_opp(self, opp_move):
        opp_attacks = opp_move.attacks
        opp_blocks = opp_move.blocks

        self.all_opp_attacks.append(tuple(opp_attacks))
        self.all_opp_blocks.append(tuple(opp_blocks))

        for attack in opp_attacks:
            self.opp_attack_pattern[attack] += BOT_REACTION_ADJ

        for block in set(opp_blocks):
            self.opp_block_pattern[block] += BOT_REACTION_ADJ

        for k, v in self.opp_block_pattern.iteritems():
            if v - BOT_DEGRADATION >= 0:
                self.opp_block_pattern[k] -= BOT_DEGRADATION
            else:
                self.opp_block_pattern[k] = 0

        for k, v in self.opp_attack_pattern.iteritems():
            if v - BOT_DEGRADATION >= 0:
                self.opp_attack_pattern[k] -= BOT_DEGRADATION
            else:
                self.opp_attack_pattern[k] = 0

        self.turn_number += 1

    def make_next_move(self,
                       opponents_last_move,
                       my_last_score,
                       opponents_last_score):

        if opponents_last_move is not None:
            self.analyze_opp(opponents_last_move)

        predicted_attack = predicted_block = None

        if self.turn_number > 4:
            predicted_attack = predict_next_move(self.all_opp_attacks)
            predicted_block = predict_next_move(self.all_opp_blocks)

            move = Move()
            moves = 0
            if predicted_attack is not None:
                move.add_block(predicted_attack)
                moves += 1

            if predicted_block is not None:
                move.add_attack(weighted_choice((x, y) for x, y in attack_points.iteritems() if x != predicted_block))
                moves += 1

            if moves > 0:
                for i in range(3 - moves):
                    move.add_attack(self.get_attack())
                return move


        return self.create_move()


if __name__ == '__main__':
    codefights.boilerplate.SDK.SDK.run(Fighter, argv)
    #codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-me"])

    print("Kickboxer:")
    #codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "kickboxer"])
    print("Boxer:")
    #codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "boxer"])
    print("Laura++:")
    #codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "laura++"])
    print("PeeGrabber:")
    #codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "peegrabber"])
