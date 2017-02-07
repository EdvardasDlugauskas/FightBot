from __future__ import division
from codefights.model.IFighter import *
import codefights.boilerplate.SDK
import random
import sys

class Fighter(IFighter):
    def make_next_move(self,
                       opponents_last_move,
                       my_last_score,
                       opponents_last_score):

        return random.choice([Move().add_attack("NOSE").add_attack("NOSE").add_block("JAW"),
                       Move().add_attack("JAW").add_attack("JAW").add_block("NOSE")])

if __name__ == '__main__':
    codefights.boilerplate.SDK.SDK.run(Fighter, sys.argv)
    #codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-me"])

    print("Kickboxer:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "kickboxer"])
    print("Boxer:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "boxer"])