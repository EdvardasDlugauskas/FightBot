from codefights.model.IFighter import *
import codefights.boilerplate.SDK
import sys
from random import randint, choice


class Fighter(IFighter):
    attacked_same_place_twice = False

    move_points = {
        "NOSE": 10,
        "JAW": 8,
        "BELLY": 8,
        "GROIN": 4,
        "LEGS": 1
    }

    opp_attack_pattern = {
        "NOSE": 0,
        "JAW": 0,
        "BELLY": 0,
        "GROIN": 0,
        "LEGS": 0
    }

    opp_block_pattern = {
        "NOSE": 0,
        "JAW": 0,
        "BELLY": 0,
        "GROIN": 0,
        "LEGS": 0
    }

    def get_weights(self):
        return [(name, points) for name, points in self.move_points.iteritems()]

    def create_move(self):
        move = Move()
        moves_left = 3

        if self.attacked_same_place_twice:
            blocks = self.best_blocks()
            if len(blocks) == 1:
                move.add_block(blocks[0])
                moves_left -= 1

            elif len(blocks) == 2:
                move.add_block(blocks[0])
                move.add_block(blocks[1])
                moves_left -= 2

        for i in range(moves_left):
            move.add_attack(self.best_attack())

        return move

    def best_attack(self):
        distr = []
        for name, times_blocked in self.opp_block_pattern.iteritems():
            points = times_blocked * self.move_points[name]
            distr.append((name, points))

        min_points = min(distr, key=lambda x: x[1])
        best_attacks = [x[0] for x in distr if x[1] < (min_points[1] * 5/4)]
        if not best_attacks:
            return choice(self.move_points.keys())

        return choice(best_attacks)


    def best_blocks(self):
        distr = []
        for name, times_attacked in self.opp_attack_pattern.iteritems():
            points = times_attacked * self.move_points[name]
            distr.append((name, points))

        max_points = max(distr, key=lambda x: x[1])
        return [x[0] for x in distr if x[1] > (max_points[1] * 3/4)]

    def analyze_opp(self, opp_move):
        opp_attacks = opp_move.attacks
        opp_blocks = opp_move.blocks
        if len(opp_attacks) != len(set(opp_attacks)):
            self.attacked_same_place_twice = True

        for attack in opp_attacks:
            self.opp_attack_pattern[attack] += 1

        for block in set(opp_blocks):
            self.opp_block_pattern[block] += 1

        for k, v in self.opp_block_pattern.iteritems():
            if v >= 0:
                self.opp_block_pattern[k] -= 0.25

        for k, v in self.opp_attack_pattern.iteritems():
            if v >= 0:
                self.opp_attack_pattern[k] -= 0.25

    def make_next_move(self,
                       opponents_last_move,
                       my_last_score,
                       opponents_last_score):
        if opponents_last_move is not None:
            self.analyze_opp(opponents_last_move)

        return self.create_move()




if __name__ == '__main__':
    # Change that to sys.argv - ["", "--fight-me"]
    #codefights.boilerplate.SDK.SDK.run(Fighter, sys.argv)
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-me"])