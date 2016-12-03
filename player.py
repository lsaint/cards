import random

from rule import *
from card import Cards,Card, upper


PLAY_FIRST = "first"
PLAY_PASS = "pass"

class Player(object):

    def __init__(self):
        self.id = None
        self.cards = Cards([])


    def play(self, last_round):
        print("hand: %s \n" % self.cards)
        inputs = input("your turn, enter letter to play or enter p to pass:")
        check_ret = False
        while  check_ret is not True:
            if inputs.lower() == "p":
                return PLAY_PASS
            inputs = upper(inputs)
            check_ret = self.check(inputs)
            if check_ret is True:
                break
            inputs = input(check_ret)

        cards = Cards(inputs)
        self.removeCards(cards)
        return cards


    def check(self, inputs):
        if not self.cards.isContain(Cards(inputs)):
            return "played not exist card!  your turn:"
        if validate(inputs) < 0:
            return "invalid card type! your turn:"

        return True


    def removeCards(self, cards):
        self.cards.remove(cards)


    def isEmpty(self):
        return not bool(len(self.cards.strings))



class AIPlayer(Player):

    def play(self, last_round):
        ret = self.cards[random.randint(0, len(self.cards.strings)-1)]
        print("AI Player play %s" % ret)
        self.removeCards(Cards(ret))
        return ret

