import random

from rule import *
from card import Cards,Card


PLAY_FIRST = "first"
PLAY_PASS = "pass"

class Player(object):

    def __init__(self):
        self.id = None
        self.hand_cards = Cards([])


    def play(self, last_round):
        print("hand: %s \n" % self.hand_cards)
        inputs = input("your turn, enter letter to play or enter p to pass:")
        check_ret = False
        while not check_ret:
            if inputs.lower() == "p":
                return PLAY_PASS
            check_ret = self.check(inputs)
            if check_ret:
                break
            inputs = input("played not exist card!\nyour turn:")

        cards = Cards(inputs)
        self.removeCards(cards)
        return cards


    def check(self, inputs):
        return self.hand_cards.isContain(Cards(inputs))


    def removeCards(self, cards):
        self.hand_cards.remove(cards)


    def isEmpty(self):
        return not bool(len(self.hand_cards.strings))


class AIPlayer(Player):

    def play(self, last_round):
        ret = self.hand_cards[random.randint(0, len(self.hand_cards.strings)-1)]
        print("AI Player play %s" % ret)
        self.removeCards(Cards(ret))
        return ret

