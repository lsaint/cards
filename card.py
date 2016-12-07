
from rule import *

CARDS = "A234567890JQK"+"wW"


def upper(ss):
    w = ss.find('w')
    if w <  0:
        return ss.upper()
    else:
        lt = list(ss)
        lt[w] = 'w'
        return "".join(lt)


class Card(object):

    def __init__(self, c):
        if c.upper() not in CARDS:
            raise BaseException("not exists card "  + c)
        self.string = c.upper() if c != "w" else "w"


    def __str__(self):
        return self.string



class Cards(object):

    def __init__(self, ss=""):
        self.strings = upper(ss)


    def __len__(self):
        return len(self.strings)


    def __getitem__(self,index):
        return self.strings[index]


    def __str__(self):
        return self.show()


    def show(self):
        if len(self) == 0:
            return "-"
        ret = sorted(self.strings, key=sortfunc)
        return "-".join(ret)


    def append(self, item):
        self.strings += upper(item)


    def isContain(self, cards):
        return containsAll(self.strings, cards.strings)


    def remove(self, cards):
        lt = list(self.strings)
        ss = cards.strings if type(cards) == Card else cards
        for s in ss:
            lt.remove(s)
        self.strings = "".join(lt)



if __name__ == '__main__':
    cards = Cards("47AKQ")
    print(cards)

    print(cards.isContain(Cards("7AQ")))

    cards.remove(Cards("AK"))
    print(cards)
