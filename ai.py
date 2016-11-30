
# 拆牌
#  |__ 抽牌
#  |__ 组牌
#
#  手数
#  权重

import itertools
from collections import Counter
from rule import RULE_LIST, sortCardStrings



def split(count, strings):
    strings = sortCardStrings(strings)
    ret = []
    c = Counter(strings)
    for k, v in c.items():
        if v >= count:
            c = k * count
            strings = strings.replace(c, "")
            ret.append(c)
            if v == count * 2:
                # seq_4 = seq_2 * 2
                ret.append(c)
    return ret, strings


def splitL(strings):
    strings = sortCardStrings(strings)
    all_seq = []
    for i in range(5, 13)[::-1]:
        all_seq.extend(RULE_LIST["seq_single%s"%i])
    for seq in all_seq:
        if strings.find(seq) >= 0:
            return seq, strings.replace(seq, "")
    return "", strings


def split1(s):return splitL(s)
def split2(s):return split(2, s)
def split3(s):return split(3, s)
def split4(s):return split(4, s)
SPLIT_FUNC = {1: split1, 2: split2, 3: split3, 4: split4}


def genAllKindHandCards(strings):
    pmt = list(itertools.permutations(range(1, 5), 4))
    hcs = []
    for tp in pmt:
        hc = HandCards()
        s = strings
        for split_type in tp:
            lt, s = SPLIT_FUNC[split_type](s)
            hc.ship(split_type, lt)
        hc.ship(0, s)
        if len(hcs) == 0 or hc != hcs[-1]:
            hcs.append(hc)
    return hcs


class HandCards(object):

    def __init__(self):
        self.split0 = []
        self.split1 = ""
        self.split2 = []
        self.split3 = []
        self.split4 = []

        self.hands = 0
        self.weight = 0


    def __hash__(self):
        return hash(tuple([tuple(self.split0),
                            self.split1,
                            tuple(self.split2),
                            tuple(self.split3),
                            tuple(self.split4)]))


    def ship(self, split_type, ss):
        setattr(self, "split%s" % split_type, ss)


    def __str__(self):
        return "%s %s %s" % (str([self.split0, self.split1, self.split2, self.split3, self.split4]),
                                "hands:%s" % self.hands,
                                "weight:%s" % self.weight)

    def __repr__(self):
        return self.__str__()


    def __eq__(self, rhs):
        return len(self.split0) == len(rhs.split0) and\
                len(self.split1) == len(rhs.split1) and\
                len(self.split2) == len(rhs.split2) and\
                len(self.split3) == len(rhs.split3) and\
                len(self.split4) == len(rhs.split4) and\
                self.hands == rhs.hands and\
                self.weight == rhs.weight




if __name__ == '__main__':
    import pprint
    import timeit

    test = "w222AAQQQQJ098766544"
    print("test", test)
    print("split(2)", split(2, test))
    print("split(3)", split(3, test))
    print("split(4)", split(4, test))
    print("splitL()", splitL(test))

    pp = pprint.PrettyPrinter()

    start = timeit.default_timer()
    ret = genAllKindHandCards(test)
    stop = timeit.default_timer()

    pp.pprint(set(ret))
    print(stop-start)
