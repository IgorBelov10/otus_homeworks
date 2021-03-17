#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------

import itertools


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
        отсортированный от большего к меньшему"""
    replacements = {
        "T": "10",
        "J": "11",
        "Q": "12",
        "K": "13",
        "A": "14"
    }

    result = [int(replacements.get(c, c)) for c in list(map(lambda el: el[0], hand))]
    result.sort(reverse=True)
    return result


def flush(hand):

    """Возвращает True, если все карты одной масти"""
    suits = list(map(lambda el: el[1], hand))

    return all(element == suits[0] for element in suits)


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""

    str_ranks = "".join(list(map(str, ranks)))
    for i in range(2, 11):
        street = "".join(list(str(j) for j in reversed(range(i, i + 5))))

        if street in str_ranks:
            return True

    return False


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""

    str_ranks = "".join(list(map(str, ranks)))
    for i in reversed(range(2, 15)):
        kinds = "".join(list(str(j) for j in itertools.repeat(i, n)))
        if kinds in str_ranks:
            return i
    return None


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    ranks_new = ranks.copy()
    two_pairs = list()
    two_pairs.append(kind(2, ranks_new))
    while True:
        try:
            ranks_new.remove(two_pairs[0])
        finally:
            break
    two_pairs.append(kind(2, ranks_new))
    if two_pairs[1] is None:
        return None
    else:
        return two_pairs


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    max_rank = max(list(map(hand_rank, itertools.combinations(hand, 5))))
    result = []
    for i in list(itertools.combinations(hand, 5)):
        if hand_rank(i) == max_rank:
            result.append([sum(card_ranks(i)), sorted(i)])
    return max(result)[1]


def replace_jokers(splited_hand):
    """Подменяет джокеров на все возможные карты, котоыре они могут заменить"""
    suits_red = ["D", "H"]
    suits_black = ["C", "S"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

    hand = " ".join(splited_hand)

    if "?R" in hand and "?B" in hand:
        result = list(
            hand.replace("?R", i) for i in (list(str(j[1] + j[0]) for j in itertools.product(suits_red, ranks))))
        return(list(k.replace("?B", i).split() for k in result for i in
               list(str(j[1] + j[0]) for j in itertools.product(suits_black, ranks))))
    if "?R" in hand:
        return list(
            hand.replace("?R", i).split() for i in (list(str(j[1]+j[0]) for j in itertools.product(suits_red, ranks))))
    elif "?B" in hand:
        return list(
            hand.replace("?B", i).split() for i in (list(str(j[1]+j[0]) for j in itertools.product(suits_black, ranks)))
        )
    else:
        return [hand.split()]


def remove_string_with_duplicates(hands):
    """убирает наборы карт с дублирующимися картами"""
    return list(filter(lambda i: set([x for x in i if i.count(x) > 1]) == set(), hands))


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    hands_no_jokers = remove_string_with_duplicates(replace_jokers(hand))

    max_rank = max(map(hand_rank, map(best_hand, hands_no_jokers)))
    result = []
    for i in list(map(best_hand, hands_no_jokers)):
        if hand_rank(i) == max_rank:
            result.append([sum(card_ranks(i)), sorted(i)])
    return best_hand(max(result)[1])


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
