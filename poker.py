__author__ = "Gerard van Helden <drm@melp.nl>"

import random
from itertools import combinations

DIAMONDS    = ("d", "\u2666")
SPADES      = ("s", "\u2660")
CLUBS       = ("c", "\u2663")
HEARTS      = ("h", "\u2665")
SUITS       = (HEARTS, CLUBS, SPADES, DIAMONDS)
CARDS       = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
HANDS       = ("High card", "One pair", "Two pair", "Three of a kind", "Straight", "Flush", "Full house", "Four of a kind", "Straight flush")

hand_value  = HANDS.index
card_value  = CARDS.index

def is_suited(cards):
    return all([cards[0].suit == b.suit for b in cards[1:]]);

def is_sequential(cards):
    # only check for the 4 lowest cards, because the highest might be an ace in a wheel
    if not all(cards[i].value -1 == cards[i+1].value for i in range(1, len(cards)-1)):
        return False

    return cards[0].value -1 == cards[1].value or cards[0].value % (len(CARDS) -1) == cards[-1].value
    
def grouped(cards): 
    group = dict()
    for i in cards:
        if i.value not in group:
            group[i.value] = [i.value]
        else:
            group[i.value].append(i.value)
    return sorted(group.values(), key=lambda i: len(i), reverse=True)

def kickers(cards, valueCards):
    return [value for value in cards if value not in valueCards]

def evaluate(cards):
    _value = None
    card_values = lambda: [card.value for card in cards]
    
    if len(cards) != 5:
        raise Exception("Can only determine value for 5 cards")
    if is_sequential(cards):
        if cards[-1].str_value == "2":
            # Ace counts as lower than 2 in this case, so we count the 5
            handValue = cards[1].value
        else:
            handValue = cards[0].value 

        if is_suited(cards):
            _value = (hand_value("Straight flush"), [handValue])
        else:
            _value = (hand_value("Straight"), [handValue])
    elif is_suited(cards):
        _value = (hand_value("Flush"), card_values())
    else:
        groups = grouped(cards)
        groupCount = len(groups)
        
        if groupCount == 5:
            _value = (hand_value("High card"), card_values())
        elif groupCount == 4:
            _value = (hand_value("One pair"), [groups[0][0]] + kickers(card_values(), groups[0]))
        elif groupCount == 3:
            if len(groups[0]) == 3:
                _value = (hand_value("Three of a kind"), [groups[0][0]] + kickers(card_values(), groups[0]))
            else:
                # higher pair counts, then lower pair, then kicker
                pairValues = sorted([c[0] for c in groups if len(c) > 1], reverse=True)
                _value = (hand_value("Two pair"), pairValues + kickers(card_values(), groups[0] + groups[1]))
        elif groupCount == 2:
            if len(groups[0]) == 3 and len(groups[1]) == 2:
                # part of 3 counts, part of 2 kicks
                _value = (hand_value("Full house"), [groups[0][0], groups[1][0]])
            else:
                _value = (hand_value("Four of a kind"), [groups[0][0]] + kickers(card_values(), groups[0]))
        else:
            pass # 1 group is not possible, exception will be thrown
    if _value == None:
        raise Exception("Indeterminable value: " + str(self))

    return _value    

class Card:
    def from_str(s):
        return Card([suit for suit in SUITS if suit[0] == s[-1]].pop(), s[0:-1])

    def __init__(self, suit, value):
        if not suit in SUITS:
            raise Exception("Invalid suit")
        if not value in CARDS:
            raise Exception("Invalid value")

        self.suit = suit
        self.value = card_value(value)
        
    def __str__(self):
        return CARDS[self.value] + self.suit[1]

    def __lt__(self, card):
        return self.value < card.value
        
    def __int__(self):
        return self.value
        
    str_value = property(lambda self: CARDS[self.value], None)
        
    
        
class Hand:
    def from_str(s):
        c = []
        while len(s) > 0:
            cs = s[0:2]
            if cs == "10":
                cs = s[0:3]
                s = s[3:]
            else:
                s = s[2:]
            c.append(Card.from_str(cs))
        return Hand(c)

    def __init__(self, cards):
        self.cards = cards
        self.cards.sort(reverse=True)
        self._value = None

    def getvalue(self):
        if self._value == None:
            self._value = evaluate(self.cards)
        return self._value
        
    value = property(getvalue, None)

    def __str__(self):
        return "".join(map(str, self.cards))
        
    def __lt__(self, hand):
        lval = self.value
        rval = hand.value

        if lval[0] < rval[0]:
            return True
        elif lval[0] == rval[0]:
            for i, val in enumerate(lval[1]):
                if val < rval[1][i]:
                    return True
        return False
   
class Deck:
    def __init__(self, suits=SUITS, values=CARDS):
        self.cards = []
        for s in suits:
            for v in values:
                self.cards.append(Card(s, v))
                
    def shuffle(self):
        random.shuffle(self.cards)
        
    def sort(self):
        self.cards.sort()

    def __iter__(self):
        return iter(self.cards)
        
    def pop(self):
        return self.cards.pop();
        
    def __str__(self):
        return "\n".join(map(str, self._cards))
        

class Game:
    def __init__(self, deck, players):
        self._deck = deck
        self._players = players
        self.board = []
        
    def addPlayer(self, p):
        self._players.append(p)
        
    def deal(self):
        self._deck.shuffle()
        for i in range(0, 2):
            for p in self._players:
                p.deal(self._deck.pop())
                
    def flop(self):
        self._dealBoard(3)
    
    def turn(self):
        self._dealBoard(1)
        
    def river(self):
        self._dealBoard(1)
        
    def _dealBoard(self, n):
        for i in range(0, n):
            self.board.append(self._deck.pop())
                
    def __str__(self):
        s = "The board is: %s" % " ".join(map(str, self.board)) + "\n"
        for (i, p) in enumerate(self._players):
            s += "Player %d has %s, playing hand %s" % (i, p, p.hand(self)) + "\n"
        return s

class Player:
    def __init__(self):
        self._hand = []

    def deal(self, card):
        self._hand.append(card)
        
    def __str__(self):
        return " ".join(map(str, self._hand))
        
    def hand(self, board):
        possible_hands = []
        possible_hands.append(Hand(board))
        for c in combinations(board, 4):
            possible_hands.append(Hand([self._hand[0]] + list(c)))
            possible_hands.append(Hand([self._hand[1]] + list(c)))
        for c in combinations(board, 3):
            possible_hands.append(Hand(self._hand + list(c)))
        possible_hands.sort()
        return possible_hands.pop()
        
if __name__ == "__main__":
    print("Generating available hands")
#    hands = list(map(Hand, map(list, combinations(Deck(suits=(DIAMONDS, HEARTS)).cards, 5))))
    hands = list(map(Hand, map(list, combinations(Deck().cards, 5))))
    print("%d hands generated. Shuffling..." % len(hands))
    random.shuffle(hands)
    print("Sorting...")
    hands.sort()
    print("Done. Lowest hand is %s, highest hand is %s" % (hands[0], hands[-1]))
#    for h in hands:
#        print(h)

