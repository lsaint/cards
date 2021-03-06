import random, sys

from state_machine import *

from player import *
from ai import AIPlayer
from card import Card, Cards



POKERS_AMOUNT = 54
POKERS = list("A234567890JQK" * 4 + "wW")
MAX_PLAYER = 2
TWO_PLAYER_CARD_NUM = 40


@acts_as_state_machine
class Table(object):

    waiting = State(initial=True)
    dealing = State()
    player1 = State()
    player2 = State()
    gameover = State()

    wait = Event(from_states=gameover, to_state=waiting)
    deal = Event(from_states=waiting, to_state=dealing)
    p1 = Event(from_states=(player2, dealing), to_state=player1)
    p2 = Event(from_states=player1, to_state=player2)
    over = Event(from_states=(player1, player2), to_state=gameover)

    # p1 always play first

    def __init__(self):
        self.players = []


    @before("deal")
    def checkPlayer(self):
        if len(self.players) != MAX_PLAYER:
            print("not enough player")
            return False
        self.prepare()


    def prepare(self):
        #random.shuffle(self.players)
        self.player1 = self.players[0]
        self.player1.id = 1
        self.player2 = self.players[1]
        self.player2.id = 2
        self.last_round = PLAY_FIRST


    @after("deal")
    def doDeal(self):
        count = 0
        random.shuffle(POKERS)
        for i, v in enumerate(POKERS):
            self.players[i % MAX_PLAYER].pick(POKERS[i])
            count += 1
            if count == TWO_PLAYER_CARD_NUM:
                break
        self.players[0].card_strings = "708AQJW7709A5QQ247JJ"   # test
        print("AI raw:", self.players[0].card_strings)
        for player in self.players:
            player.readyPlay()
        self.p1()


    def doPlay(self, p):
        try:
            self.last_round = self.players[p-1].play(self.last_round)
        except KeyboardInterrupt:
            sys.exit()
        if self.players[p-1].isEmpty():
            return self.over()
        self.p1() if p == 2 else self.p2()


    @after("p1")
    def play1(self):
        self.doPlay(1)


    @after("p2")
    def play2(self):
        self.doPlay(2)


    @after("over")
    def doGameOver(self):
        print("Winner is player%d" % (1 if self.player1.isEmpty() else 2))
        print()
        input("press any key to continue..")
        self.start()


    @after("wait")
    def doWait(self):
        input("press any key to start game..")
        self.deal()


    def start(self):
        self.players = [AIPlayer(), Player()]
        self.deal()
        print("game started")


if __name__ == "__main__":
    t = Table()
    t.start()

