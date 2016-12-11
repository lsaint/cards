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
import functools
import random
from collections import Counter

from rule import *
from card import Cards
from player import PLAY_FIRST, PLAY_PASS


def probability(num):
    return random.randint(1, 100) <= num


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
    def trimSeq(l, seq):
        ret = []
        l = l
        while l.find(seq) >= 0:
            ret.append(seq)
            l = l.replace(seq, "")
        return l, ret

    strings = sortCardStrings(strings)
    # remove same cards
    str_set = sortCardStrings("".join(set(strings)))
    # cards removed
    df = strDelDiff(strings, str_set)
    ret = []
    for seq in ALL_SEQ:
        str_set, r1 = trimSeq(str_set, seq)
        ret.extend(r1)
        df, r2 = trimSeq(df, seq)
        ret.extend(r2)
    return ret, str_set + df



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


def sortHandCards(hca, hcb):
    if hca.hands == hcb.hands:
        return hcb.weight - hca.weight
    else:
        return hca.hands - hcb.hands



class HandCards(Cards):

    def __init__(self, strings):
        super().__init__(strings)
        self.split0 = []    # single
        self.split1 = []    # single-seq
        self.split2 = []    # pair
        self.split3 = []    # trio
        self.split4 = []    # bomb
        self.split22 = []   # pair-seq
        self.split33 = []   # trio-seq
        self.rocket = []
        self.name_split ={}

        self.seq2_weight = 0    # pair-seq weight
        self.seq3_weight = 0    # trio-seq weight

        self.hands = 0
        self.weight = 0


    def __hash__(self):
        return hash(tuple([tuple(self.split0),
                            tuple(self.split1),
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


    def remove(self, cards):
        super().remove(cards)
        if len(cards) >= 4:
            cards.resloveRelatedCards()
        t = cards.ctype
        if t[-1].isdigit():
            t = t[0:-1]
        lt = self.name_split[t]
        lt.remove(cards.strings)

        rel = cards.related
        if rel:
            for ss in related:
                if len(ss) == 1:
                    self.split0.remove(ss)
                else:
                    self.split2.remove(ss)


    def ship(self, split_type, ss):
        setattr(self, "split%s" % split_type, ss)


    def splitRocket(self, strings):
        if ROCKET in strings:
            self.rocket = [ROCKET]
            return strings.replace(ROCKET, "")
        return strings


    def calHands(self):
        c0 = len(self.split0)
        c1 = 0 if (len(self.split1) == 0) else 1
        c2 = len(self.split2)
        c3 = len(self.split3)
        c4 = len(self.split4)
        c22 = len(self.split22)
        c33 = len(self.split33)
        self.hands = c0 + c1 + c2 + c3 + c4 + c22 + c33 - self.calTrioRelated()
        return self.hands


    def calTrioRelated(self):
        # trio with 1 single or 1 pair
        h = len(self.split0) + len(self.split2)
        trio = len(self.split3)
        for seq in self.split33:
            trio += len(seq) / 3
        return trio if trio <= h else h


    def calWeight(self):
        c0 = len(self.split0)
        c1 = 0
        for seq in self.split1:
            c1 += len(seq) - 1
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
        self.name_split = {"single": self.split0, "pair": self.split2,
                            "trio": self.split3, "bomb": self.split4,
                            "seq_single": self.split1,
                            "seq_pair": self.split22,
                            "seq_trio": self.split33,
                            "rocket": self.rocket}  # shiped



class AIPlayer(object):

    def __init__(self):
        self.cardStrings = ""
        self.handcards = []
        self.hc = None


    def pick(self, s):
        self.cardStrings += s


    def readyPlay(self):
        self.genAllKindHandCards()


    def isEmpty(self):
        return not bool(len(self.hc.strings))


    def genAllKindHandCards(self):
        pmt = list(itertools.permutations(range(1, 5), 4)) # 排列
        hcs = []
        for tp in pmt:
            hc = HandCards(self.cardStrings)
            s = self.cardStrings
            for split_type in tp:
                lt, s = SPLIT_FUNC[split_type](s)
                hc.ship(split_type, lt)
            s = hc.splitRocket(s)
            hc.ship(0, list(s))
            if len(hcs) == 0 or hc != hcs[-1]:
                hcs.append(hc)
        hcs = set(hcs)
        for hc in hcs:
            hc.cal()
        self.handcards = sorted(list(hcs), key=functools.cmp_to_key(sortHandCards))
        self.hc = self.handcards[0]


    def getRelatedCards(self, count=1):
        # when play trio or trio-seq, decide which cards to take with
        exclude = set(['A', '2', 'w', 'W'])
        if len(self.hc.split0) >= count:
            ret = self.hc.split0[0:count]
            if not set(ret).intersection(exclude):
                return ret

        exclude = set(['KK', 'AA', '22'])
        if len(self.hc.split22) >= count:
            ret = self.hc.split22[0:count]
            if not set(ret).intersection(exclude):
                return ret

        return ""


    # 主动出牌
    def initiativePlay(self):
        # .pair-seq
        if self.hc.split22:
            return self.hc.split22[0]
        # .single-seq
        if self.hc.split1:
            return self.hc.split1[0]
        # .trio
        if self.hc.split3:
            rel = self.getRelatedCards()
            ret = self.hc.split3[0] + rel
            return ret
        # .trio-seq
        if self.hc.split33:
            rel = self.getRelatedCards(2)
            ret = self.hc.split33[0] + rel
            return ret

        holding = ""
        # .pair
        if self.hc.split2:
            p = self.hc.split2[0]
            if p not in ("22",):
                return p
            holding = p
        # .single
        if self.hc.split0:
            s = self.hc.split0[0]
            if s not in ("2", "w", "W"):
                return s
            holding = s
        return holding


    # 被动出牌
    def passivePlay(self, last_round):
        pass


    def play(self, last_round):
        #if last_round in (PLAY_FIRST, PLAY_PASS):
        #    ret = self.initiativePlay()
        #else:
        #    ret = self.passivePlay(last_round)
        print("AI", self.hc)
        p = self.initiativePlay()
        v = cardStringsValue(p)
        ret = Cards(p, v[0], v[1]) # test
        self.hc.remove(ret)
        print("play", ret)
        return ret




if __name__ == '__main__':
    import pprint
    import timeit

    test = "w222AAQQQJJJ098766544"
    #test = "22AAKQJ9987776654"
    #test = "3456790JQKA"
    print("test", test)
    print("split(2)", split(2, test))
    print("split(3)", split(3, test))
    print("split(4)", split(4, test))
    print("splitL()", splitL(test))
    print()

    pp = pprint.PrettyPrinter()
    aip = AIPlayer()
    aip.cardStrings = test

    start = timeit.default_timer()
    ret = aip.genAllKindHandCards()
    stop = timeit.default_timer()
    pp.pprint(aip.handcards)
    print(stop-start)

    print("\n", aip.getRelatedCards())
    print("\n", aip.hc.show())

