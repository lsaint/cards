
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
    '''cards in player's hand or played cards'''

    def __init__(self, ss="", ctype=None, value=None):
        self.strings = upper(ss)

        self.ctype = ctype
        self.value = value
        self.related = []
        self.rel_type = None


    def __len__(self):
        return len(self.strings)


    def __getitem__(self,index):
        return self.strings[index]


    def __str__(self):
        return self.show()


    def resloveRelatedCards(self):
        if self.ctype == "trio_single":
            self.related = [self.strings[4]]
            self.rel_type = RT_SINGLE
        elif self.ctype == "trio_pair":
            self.related = [self.strings[3:4]]
            self.related = RT_PAIR
        elif self.ctype == "bomb_pair":
            self.related = [self.strings[3:4], self.strings[5:6]]
            self.rel_type = RT_PAIR2
        elif self.ctype == "bomb_single":
            self.related = [self.strings[4], self.strings[5]]
            self.rel_type = RT_SINGLE2
        for r in self.related:
            self.strings = self.strings.replace(r, "")


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

    print()
    cards = Cards("AAAA34", "bomb_single")
    cards.resloveRelatedCards()
    print(cards.strings, cards.related)
