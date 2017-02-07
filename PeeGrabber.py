from __future__ import division
from codefights.model.IFighter import *
import codefights.boilerplate.SDK
import random
import sys

BOT_REACTION_ADJ = 4
BOT_DEGRADATION = 1


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
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


class PeeGrabber(IFighter):
    defend = False
    turn_number = 1

    attack_points = {
        "NOSE": 0,
        "JAW": 0,
        "BELLY": 6,
        "GROIN": 4,
        "LEGS": 3
    }

    block_points = {
        "NOSE": 10,
        "JAW": 8,
        "BELLY": 6,
        "GROIN": 4,
        "LEGS": 0
    }

    opp_attack_pattern = {
        "NOSE": 10,
        "JAW": 8,
        "BELLY": 6,
        "GROIN": 4,
        "LEGS": 0
    }

    opp_block_pattern = {
        "NOSE": 10,
        "JAW": 8,
        "BELLY": 6,
        "GROIN": 4,
        "LEGS": 0
    }

    def create_move(self):
        move = Move()

        focused_areas = self.best_blocks()
        best_blocks_sorted = sorted(focused_areas, key=lambda x: x[1], reverse=True)

        if len(focused_areas) == 1 and self.defend:
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

        return move


    def get_attack(self):
        probs = probabilities(self.opp_block_pattern)
        scores = []
        for name, prob in probs.iteritems():
            scores.append((name, self.attack_points[name] * (1 - prob)))

        return weighted_choice(scores)

    def get_block(self):
        probs = probabilities(self.opp_attack_pattern)
        scores = []
        for name, prob in probs.iteritems():
            scores.append((name, self.block_points[name] * prob))

        return weighted_choice(scores)

    def best_blocks(self):
        probs = probabilities(self.opp_attack_pattern)
        scores = []
        for name, prob in probs.iteritems():
            if name not in ["LEGS", "GROIN", "BELLY"]:
                scores.append((name, self.block_points[name] * prob))

        max_points = sum([x for y, x in scores])
        return [x for x in scores if x[1]/max_points > 0.33]

    def analyze_opp(self, opp_move):
        if len(opp_move.attacks) != len(set(opp_move.attacks)):
            self.defend = True

        opp_attacks = opp_move.attacks
        opp_blocks = opp_move.blocks

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

        if random.randint(0, 4) == 0:
            move = Move()
            attack = random.choice(("NOSE", "JAW"))
            move.add_attack(attack)
            move.add_attack(attack)
            move.add_attack(attack)
            return move

        return self.create_move()


if __name__ == '__main__':
    codefights.boilerplate.SDK.SDK.run(PeeGrabber, sys.argv)
    #codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-me"])

    print("Kickboxer:")
    codefights.boilerplate.SDK.SDK.run(PeeGrabber, ["", "--fight-bot", "kickboxer"])
    print("Boxer:")
    codefights.boilerplate.SDK.SDK.run(PeeGrabber, ["", "--fight-bot", "boxer"])
    print("Laura++:")
    codefights.boilerplate.SDK.SDK.run(PeeGrabber, ["", "--fight-bot", "laura++"])
