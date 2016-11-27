
from rule import *

CARDS = "A234567890JQK"+"wW"

class Card(object):

    def __init__(self, c):
        if c.upper() not in CARDS:
            raise BaseException("not exists card "  + c)
        self.string = c.upper() if c != "w" else "w"


    def __str__(self):
        return self.string



class Cards(list):

    def __init__(self, strings):
        list.__init__([])
        self.strings = ""
        for s in strings:
            self.append(Card(s))


    def append(self, item):
        if not isinstance(item, Card):
            raise TypeError('Card type only')
        super(Cards, self).append(item)
        self.strings += str(item)


    def __str__(self):
        if len(self) == 0:
            return "-"
        ret = sorted(self.strings, key=sortfunc)
        return "-".join(ret)


    def isContain(self, cards):
        return containsAll(self.strings, cards.strings)


    def remove(self, cards):
        lt = list(self.strings)
        for s in cards.strings:
            lt.remove(s)
        self.strings = "".join(lt)



if __name__ == '__main__':
    cards = Cards("47AKQ")
    print(cards)

    print(cards.isContain(Cards("7AQ")))

    cards.remove(Cards("AK"))
    print(cards)
