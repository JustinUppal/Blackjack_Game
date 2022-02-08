import random
import sys
from collections import namedtuple
from collections import defaultdict
import csv

Score = namedtuple('Score', 'total, soft_ace_count')
Stand = namedtuple('Stand', 'stand, total')


class Hand:
    """
    Class that encapsulates a blackjack hand

    """

    def __init__(self, cards=None):
        self.total = 0
        self.soft_ace_count = 0
        self.cards = cards
        if cards is None:
            self.cards = []
        else:
            self.score()

    def __str__(self):
        return f'Hand: cards = {self.cards} and total = {self.total}'

    def add_card(self):
        self.cards.append(random.randint(1, 13))
        self.score()

    def is_blackjack(self):
        if self.total == 21:
            return True
        else:
            return False

    def is_bust(self):
        if self.total > 21:
            return True
        else:
            return False

    def score(self):
        self.total = 0
        self.soft_ace_count = 0
        for c in self.cards:
            if c == 1:
                self.total += 11
                self.soft_ace_count += 1
            elif c > 10:
                self.total += 10
            else:
                self.total += c

        # now deal with aces
        while self.total > 21 and self.soft_ace_count > 0:
            self.total -= 10
            self.soft_ace_count -= 1

        # return the current total and the number of remaining soft aces
        return tuple((self.total, self.soft_ace_count))


class Strategy:
    def __init__(self, stand_on_value, stand_on_soft):
        self.stand_on_value = stand_on_value
        self.stand_on_soft = stand_on_soft
        self.soft_ace_count = int()

    def __repr__(self):
        return f"Strategy {self.stand_on_value},{self.stand_on_soft}"

    def __str__(self):
        if self.stand_on_soft:
            return f'H{self.stand_on_value}'
        if self.stand_on_soft is False:
            return f'S{self.stand_on_value}'

    def stand(self, hand):
        if hand.total >= self.stand_on_value and self.stand_on_soft is True:
            return True
        if hand.total < self.stand_on_value and self.stand_on_soft is True:
            return False
        if hand.total < self.stand_on_value and self.stand_on_soft is False:
            return False
        if hand.total == self.stand_on_value and self.soft_ace_count >= 1 and self.stand_on_soft is False:
            return False
        if hand.total > self.stand_on_soft and self.stand_on_soft is False:
            return True

    def play(self):
        hand = Hand()
        hand.add_card()
        hand.add_card()
        while self.stand(hand) is False:
            hand.add_card()
        return hand


# def get_card():
#     """
#     returns a random integer between 1 and 13
#     """
#     return random.randint(1, 13)
#
#
# def score(cards):
#     """
#     takes a list [cards] , which can be the function get_card() as many times as you please.
#
#     """
#     soft_ace_count = 0
#     for i in range(len(cards)):
#         if cards[i] > 10:
#             cards[i] = 10
#         if cards[i] == 1 and sum(cards) < 21:
#             cards[i] = 11
#             soft_ace_count += 1
#     total = sum(cards)
#     while total > 21 and soft_ace_count > 0:
#         total -= 10
#         soft_ace_count -= 1
#
#     return tuple((total, soft_ace_count))
#
#
# def stand(stand_on_value, stand_on_soft, cards):
#     """
#     Takes the total and soft ace count (how many ace's value are 11), then returns a namedtuple called Stand,
#     Stand has two parameters, stand and total.
#     Yes, the stand function returns a Stand tuple with a Boolean parameter called stand.
#
#     """
#
#     total, soft_ace_count = score(cards)
#     if total >= stand_on_value and stand_on_soft is True:
#         return Stand(True, total)
#     if total < stand_on_value and stand_on_soft is True:
#         return Stand(False, total)
#     if total < stand_on_value and stand_on_soft is False:
#         return Stand(False, total)
#     if total == stand_on_value and soft_ace_count >= 1 and stand_on_soft is False:
#         return Stand(False, total)
#     if total > stand_on_soft and stand_on_soft is False:
#         return Stand(True, total)
#
#
# def play_hand(stand_on_value, stand_on_soft):
#     """
#     Plays a hand of blackjack. https://www.addictioncenter.com/drugs/gambling-addiction/
#     """
#     cards = [get_card(), get_card()]
#     current_hand = stand(stand_on_value, stand_on_soft, cards)
#     while current_hand.stand is False:
#         cards.append(get_card())
#         current_hand = stand(stand_on_value, stand_on_soft, cards)
#     if current_hand.total >= 22:
#         return 22
#     return current_hand.total
#
#
def main():
    """
    creates a dictionary of all the win percentages then appends them to a list then writes the list.
    """
    n = int(sys.argv[1])
    writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
    writer.writerow(['P-Strategy', 'D-H13', 'D-S13', 'D-H14', 'D-S14', 'D-H14',
                     'D-H15', 'D-S15', 'D-H16', 'D-S16', 'D-H17', 'D-S17', 'D-H18', 'D-S18', 'D-H19',
                     'D-S19', 'D-H20', 'D-S20'])
    strat_list = []
    for i in range(13, 21):
        strat_list.append(Strategy(i, False))
        strat_list.append(Strategy(i, True))
    strat_list2 = strat_list

    for player_strat in strat_list:
        percentage_winrate = defaultdict(float)
        for dealer_strat in strat_list2:
            pushes = 0
            for j in range(n):
                player_hand = player_strat.play()
                score_of_player = player_hand.total
                if not player_hand.is_bust():
                    dealer_hand = dealer_strat.play()
                    score_of_dealer = dealer_hand.total
                    if dealer_hand.is_bust():
                        percentage_winrate[dealer_strat.__str__()] += 1
                        continue
                    if player_hand.is_blackjack() and not dealer_hand.is_blackjack():
                        percentage_winrate[dealer_strat.__str__()] += 1
                    if player_hand.total == dealer_hand.total:
                        pushes += 1
                        continue
                    if score_of_player > score_of_dealer:
                        percentage_winrate[dealer_strat.__str__()] += 1
        write_list = [player_strat.__str__()]
        for k, v in percentage_winrate.items():
            percentage_winrate[k] = ((v / (n - pushes)) * 100)
            write_list.append(percentage_winrate[k])
        writer.writerow(write_list)








#
if __name__ == "__main__":
    main()
