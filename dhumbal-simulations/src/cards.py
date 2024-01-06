from enum import Enum
import random

class Result(Enum):
    DHUMBAL = 0
    GOT_DESTROYED = 1
    DESTROYED = 2
    NORMAL = 3
    
class Suit(Enum):
    SPADES = '♠'
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    NONE = ''

class Value(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    JOKER = 0


class Card:
    def __init__(self, rank: Value, suit: Suit):
        self.rank = rank
        self.suit = suit
    def __str__(self):
        return f'{self.rank.name}{self.suit.value}'

class Deck:
    def __init__(self):
        self.cards = self.generate_deck()
        self.shuffle_deck()

    def generate_deck(self):
        deck = []
        for suit in Suit:
            for rank in Value:
                if rank != Value.JOKER and suit != Suit.NONE:
                    card = Card(rank, suit)
                    deck.append(card)
        for _ in range(2):
            card = Card(Value.JOKER, Suit.NONE)
            deck.append(card)
        return deck
    
    def shuffle_deck(self):
        random.shuffle(self.cards)
        
if __name__ == '__main__':
    deck = Deck()
    print(deck.cards)
