import random

from rule import *
from card import Cards,Card, upper


PLAY_FIRST = "first"
PLAY_PASS = "pass"

class Player(object):

    def __init__(self):
        self.id = None
        self.cards = Cards()


    def pick(self, card):
        self.cards.append(card)


    def readyPlay(self):
        pass


    def play(self, last_round):
        print("hand: %s \n" % self.cards)
        inputs = input("your turn, enter letter to play or enter p to pass:")
        check_ret = False
        while  check_ret is not True:
            if inputs.lower() == "p":
                return PLAY_PASS
            inputs = upper(inputs)
            check_ret, v = self.check(inputs)
            if check_ret is True:
                cards = Cards(inputs, v[0], v[1])
                self.removeCards(cards)
                return cards
            inputs = input(v)


    def check(self, inputs):
        if not self.cards.isContain(Cards(inputs)):
            return False, "played not exist card!  your turn:"
        v = cardStringsValue(inputs)
        if v[1] <= 0:
            return False, "invalid card type! your turn:"

        return True, v


    def removeCards(self, cards):
        self.cards.remove(cards)


    def isEmpty(self):
        return not bool(len(self.cards.strings))



#class AIPlayer(Player):
#
#    def play(self, last_round):
#        ret = self.cards[random.randint(0, len(self.cards.strings)-1)]
#        print("AI Player play %s" % ret)
#        self.removeCards(Cards(ret))
#        return ret

