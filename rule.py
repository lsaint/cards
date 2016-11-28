from collections import Counter
import json

CARD_TYPE = [
    #'rocket', 'bomb',
    'single', 'pair', 'trio', 'trio_pair', 'trio_single',
    'seq_single5', 'seq_single6', 'seq_single7', 'seq_single8', 'seq_single9', 'seq_single10', 'seq_single11', 'seq_single12',
    'seq_pair3', 'seq_pair4', 'seq_pair5', 'seq_pair6', 'seq_pair7', 'seq_pair8', 'seq_pair9', 'seq_pair10',
    'seq_trio2', 'seq_trio3', 'seq_trio4', 'seq_trio5', 'seq_trio6',
    'seq_trio_pair2', 'seq_trio_pair3', 'seq_trio_pair4', 'seq_trio_pair5',
    'seq_trio_single2', 'seq_trio_single3', 'seq_trio_single4', 'seq_trio_single5',
    'bomb_pair', 'bomb_single'
]
ROCKET = "wW"
MAX_VALUE   = 3737
MIN_VALUE   = -4466
BOMB_VALUE  = 1000


with open('rule.json', 'r') as f:
    RULE_LIST = json.load(f)


def sortfunc(a):
    return '34567890JQKA2wW'.index(a)


def findRuleType(rule_type_lt, strings):
    if len(rule_type_lt[0]) != len(strings):
        return -1
    for i, e in enumerate(rule_type_lt):
        if e == strings:
            return i
    return -1


def cardStringsValue(strings):
    strings = ''.join(sorted(strings, key=sortfunc))

    if strings == ROCKET:
        return ('rocket', MAX_VALUE)

    value = findRuleType(RULE_LIST['bomb'], strings)
    if value >= 0:
        return ('bomb', BOMB_VALUE + value)

    for t in CARD_TYPE:
        value = findRuleType(RULE_LIST[t], strings)
        if value >= 0:
            return (t, value)

    return ('', 0)


# result > 0 is sucess
def validate(strings):
    value = cardStringsValue(strings)
    if value[0] == '':
        return MIN_VALUE
    return value[1]


def compare(strings_a, strings_b):
    valueA = cardStringsValue(strings_a)
    valueB = cardStringsValue(strings_b)
    if valueA[0] == valueB[0]:
        return valueA[1] - valueB[1]

    if valueA[1] >= BOMB_VALUE:
        return valueA[1] - valueB[1]
    else:
        return 0


def containsAll(parent, child):
    parent, child = Counter(parent), Counter(child)
    for k, n in child.items():
        if k not in parent or n > parent[k]:
            return False
    return True


if __name__ == '__main__':
    print("validate('0000AAJJ')", validate('0000AAJJ')) # sucess
    print("validate('KK33')", validate('KK33'))         # fail

    print('compare("AAAK", "5552")', compare('AAAK', '5552'))
    print('cardStringsValue("AAAA")', cardStringsValue('AAAA'))

    print('compare("A", "K")', compare('A', 'K'))

