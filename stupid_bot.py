from __future__ import division
from codefights.model.IFighter import *
import codefights.boilerplate.SDK
import random
import sys


class Jess(IFighter):
    defence = Move().add_block("NOSE").add_block("JAW").add_block("BELLY")
    belly = Move().add_attack("BELLY").add_attack("BELLY").add_attack("BELLY")
    nose = Move().add_attack("NOSE").add_attack("NOSE").add_attack("NOSE")
    jaw = Move().add_attack("JAW").add_attack("JAW").add_attack("JAW")

    def __init__(self):
        self.mode = random.choice([self.defence, self.belly, self.nose, self.jaw])
        random.seed()

    def make_next_move(self,
                       opponents_last_move,
                       my_last_score,
                       opponents_last_score):
        move = Move()
        for i in range(random.randint(0, 3)):
            if random.randint(0, 3):
                move.add_attack(random.choice(["BELLY", "NOSE", "JAW"]))
            else:
                move.add_block(random.choice(["BELLY", "NOSE", "JAW"]))
        print(len(move.attacks) + len(move.blocks))
        return move


if __name__ == '__main__':
    codefights.boilerplate.SDK.SDK.run(Jess, sys.argv)
    # codefights.boilerplate.SDK.SDK.run(Jess, ["", "--fight-me"])

    print("Laura++:")
    codefights.boilerplate.SDK.SDK.run(Jess, ["", "--fight-bot", "laura++"])
    print("Jess:")
    codefights.boilerplate.SDK.SDK.run(Jess, ["", "--fight-bot", "jess"])


    print("Kickboxer:")
    codefights.boilerplate.SDK.SDK.run(Jess, ["", "--fight-bot", "kickboxer"])
    print("Boxer:")
    codefights.boilerplate.SDK.SDK.run(Jess, ["", "--fight-bot", "boxer"])
    print("Laura:")
    codefights.boilerplate.SDK.SDK.run(Jess, ["", "--fight-bot", "laura"])
    print("PeeGrabber:")
    codefights.boilerplate.SDK.SDK.run(Jess, ["", "--fight-bot", "peegrabber"])