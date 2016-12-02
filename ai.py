# coding: utf-8

# 拆牌
#  |__ 抽牌
#  |__ 组牌
#
#  手数
#  权重
#  |__ 单张                             1
#  |__ 对子                             2
#  |__ 三带                             3
#  |__ 连牌                             4 (每多一张牌权值+1)
#  |__ 连对                             5 (每多一对牌，权值+2)
#  |__ 飞机                             6 (每对以飞机，权值在基础上+3)
#  |__ 炸弹                             7 (包括对王在内)

import itertools
import difflib
from collections import Counter
from rule import *



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
    str_set = sortCardStrings("".join(set(strings)))
    for seq in ALL_SEQ:
        if str_set.find(seq) >= 0:
            df = strDelDiff(strings, str_set)
            return seq, sortCardStrings(str_set.replace(seq, "") + df)
    return "", strings


def strDelDiff(a, b):
    ret = []
    for d in difflib.ndiff(a, b):
        if d[0] == "-":
            ret.append(d[-1])
    return "".join(ret)


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
    hcs = set(hcs)
    for hc in hcs:
        hc.cal()
    return hcs



class HandCards(object):

    def __init__(self):
        self.split0 = ""
        self.split1 = ""
        self.split2 = []
        self.split3 = []
        self.split4 = []

        self.split22 = []
        self.split33 = []

        self.seq2_weight = 0
        self.seq3_weight = 0

        self.hands = 0
        self.weight = 0


    def __hash__(self):
        return hash(tuple([tuple(self.split0),
                            self.split1,
                            tuple(self.split2),
                            tuple(self.split3),
                            tuple(self.split4)]))


    def __str__(self):
        return "%s%s%s%s%s" % (str([self.split0, self.split1, self.split2, self.split3, self.split4,
                                    self.split22, self.split33]),
                                " s2w:{}".format(self.seq2_weight),
                                " s3w:{}".format(self.seq3_weight),
                                " hands:%s" % self.hands,
                                " weight:%s" % self.weight)

    def __repr__(self):
        return self.__str__()


    def __eq__(self, rhs):
        return len(self.split0) == len(rhs.split0) and\
                len(self.split1) == len(rhs.split1) and\
                len(self.split2) == len(rhs.split2) and\
                len(self.split3) == len(rhs.split3) and\
                len(self.split4) == len(rhs.split4)


    def ship(self, split_type, ss):
        setattr(self, "split%s" % split_type, ss)


    def calHands(self):
        c0 = len(self.split0)
        c1 = 0 if (len(self.split1) == 0) else 1
        c2 = len(self.split2)
        c3 = len(self.split3)
        c4 = len(self.split4)
        c22 = len(self.split22)
        c33 = len(self.split33)
        self.hands = c0 + c1 + c2 + c3 + c4 + c22 + c33
        return self.hands


    def calWeight(self):
        c0 = len(self.split0)
        c1 = 0 if (len(self.split1) == 0) else (len(self.split1) - 1)
        c2 = len(self.split2) * 2
        c3 = len(self.split3) * 3
        c4 = len(self.split4) * 7
        self.weight = c0 + c1 + c2 + c3 + c4 + self.seq2_weight + self.seq3_weight
        return self.weight


    def calMultiSeq(self, mul, w, add):
        r = sortCardStrings(set("".join(getattr(self, "split%s"%mul))))
        seqs = findSeq(r)
        if seqs == 0:
            return
        for seq in seqs:
            rw = getattr(self, "seq%s_weight" % mul)
            setattr(self, "seq%s_weight"%mul, rw + w + (len(seq)-2) * add)

            for s in seq:
                split = getattr(self, "split%s" % mul)
                split.remove(s*mul)

            seq *= mul
            split = getattr(self, "split%s%s" % (mul, mul))
            split.append(sortCardStrings(seq))
            setattr(self, "split%s%s" % (mul, mul), split)


    def cal(self):
        self.calMultiSeq(2, 5, 2)
        self.calMultiSeq(3, 6, 3)
        self.calHands()
        self.calWeight() # at last



if __name__ == '__main__':
    import pprint
    import timeit

    test = "w222AAQQQJJJ098766544"
    print("test", test)
    print("split(2)", split(2, test))
    print("split(3)", split(3, test))
    print("split(4)", split(4, test))
    print("splitL()", splitL(test))

    pp = pprint.PrettyPrinter()

    start = timeit.default_timer()
    ret = genAllKindHandCards(test)
    stop = timeit.default_timer()

    pp.pprint(ret)
    print(stop-start)
