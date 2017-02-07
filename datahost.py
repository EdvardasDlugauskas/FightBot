from __future__ import division
from codefights.model.IFighter import *
import codefights.boilerplate.SDK
import random
import sys


class Jess(IFighter):
    def make_next_move(self,
                       opponents_last_move,
                       my_last_score,
                       opponents_last_score):

        return random.choice(
            [
                Move().add_attack("BELLY").add_attack("BELLY").add_attack("BELLY"),
                Move().add_attack("NOSE").add_attack("NOSE").add_attack("NOSE"),
                Move().add_attack("JAW").add_attack("JAW").add_attack("JAW")
            ]
        )

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