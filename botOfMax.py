from __future__ import division
import codefights
from codefights.model.IFighter import *
import codefights.boilerplate.SDK
from random import uniform
import sys

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
            if m > 0:
                if -m not in moves[j]:
                    top[i][j] += m
top = [[top[i][j] - top[j][i] for j in range(n)] for i in range(n)]
moveSet = 163, 162, 158, 39, 168  # CHANGE ONLY THIS

class Fighter(IFighter):
    def __init__(self):
        self.w = {i: 0 for i in moveSet}
        for i in range(170):
            self.changeWeights(i)
        self.names_to_points = {'NOSE': 10, 'JAW': 8, 'BELLY': 6, 'GROIN': 4, 'LEGS': 3}
        self.points_to_names = {self.names_to_points[k]: k for k in self.names_to_points}

    def changeWeights(self, move):
        for i in range(170):
            if i in self.w:
                self.w[i] -= top[move][i]

    def make_next_move(self, opponents_last_move, i_lost=None, i_scored=None):
        if opponents_last_move != None:
            opp = []
            for t in opponents_last_move.attacks:
                opp.append(self.names_to_points[t])
            for t in opponents_last_move.blocks:
                opp.append(-self.names_to_points[t])
            if sorted(opponents_last_move.blocks) != sorted(set(opponents_last_move.blocks)):
                opp += [3, 3, 3]
                opp = opp[:3]
            opp = moves.index(tuple(sorted(opp)))
            for i in self.w:
                self.w[i] *= 0.7
            self.changeWeights(opp)
        w = dict(self.w)
        for i in w:
            if w[i] < 0:
                w[i] = 0
        rnd = uniform(0, sum(w[k] for k in w))
        for m in moveSet:
            if self.w[m] > 0 and self.w[m] < rnd:
                break
            rnd -= self.w[m]
        move = Move()
        for t in moves[m]:
            if t > 0:
                move.add_attack(self.points_to_names[t])
            else:
                move.add_block(self.points_to_names[-t])
        return move


if __name__ == '__main__':
    #codefights.boilerplate.SDK.SDK.run(Fighter, sys.argv)
    #codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-me"])
    #codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-on-server"])

    print("Laura++:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "laura++"])
    print("Jess:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "jess"])
    print("Datahost:")
    codefights.boilerplate.SDK.SDK.run(Fighter, ["", "--fight-bot", "datahost"])

    #"""
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
    #"""