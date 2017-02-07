from codefights.model.IFighter import *
import codefights.boilerplate.SDK
import sys
from random import randint, choice


class Fighter(IFighter):
    memory = []

    def create_random_move(self):
        JAW = Area.JAW
        NOSE = Area.NOSE
        BELLY = Area.BELLY
        GROIN = Area.GROIN
        moves = [JAW, NOSE, GROIN]
        my_defences = [Area.JAW, Area.NOSE, Area.BELLY]
        my_attacks = [JAW, JAW, NOSE, NOSE, BELLY, GROIN]

        move = Move()

        for i in range(3):
            if not randint(0, 2):
                block = choice(my_defences)
                my_defences.remove(block)
                move.add_block(block)

            else:
                move.add_attack(choice(my_attacks))

        return move

    def make_next_move(self,
                       opponents_last_move,
                       my_last_score,
                       opponents_last_score):
        self.memory.append(opponents_last_move)
        print(len(self.memory))
        return self.create_random_move()


if __name__ == '__main__':
    # Change that to sys.argv - ["", "--fight-me"]
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-me"])