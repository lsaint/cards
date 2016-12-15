
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
        ''' eg.
            QQQA
           KQQQ
           00JJJJQQ
        '''
        ss = self.strings
        if self.ctype == "trio_single":
            if ss[0] != ss[1]:
                self.related = [ss[0]]
            else:
                self.related = [ss[-1]]
            self.rel_type = RT_SINGLE
        elif self.ctype == "trio_pair":
            if ss[0] != ss[2]:
                self.related = [ss[0:2]]
            else:
                self.related = [ss[3:5]]
            self.related = RT_PAIR
        elif self.ctype == "bomb_pair":
            if ss[0:2] == ss[2:4]:
                self.related = [ss[4:6], ss[6:8]]
            elif ss[4:6] == ss[6:8]:
                self.related = [ss[0:2], ss[2:4]]
            else:
                self.related = [ss[0:2], ss[6:8]]
            self.rel_type = RT_PAIR2
        elif self.ctype == "bomb_single":
            if ss[1:3] == ss[3:5]:
                self.related = [ss[0], ss[5]]
            elif ss[0:2] == ss[2:4]:
                self.related = [ss[4], ss[5]]
            else:
                self.related = [ss[0], ss[1]]
            self.rel_type = RT_SINGLE2
        for r in self.related:
            self.strings = ss.replace(r, "")


    def show(self):
        if len(self) == 0:
            return "-"
        rel = "".join(self.related)
        ret = sorted(self.strings + rel, key=sortfunc)
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
