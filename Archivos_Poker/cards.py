from __future__ import annotations
from helpers import shuffle, combinations, random


class Card:
    VALUES = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    def __init__(self, card:str):
        self.suit = card[-1]
        self.num = card[0:-1]
        self.value = self.VALUES[self.num] if self.num in self.VALUES else int(self.num)
    pass

    def __gt__(self, other: Card) -> bool:
        return self.value > other.value
    
    def __eq__(self, other: Card) -> bool:
        if isinstance(other, Card):
            return self.num == other.num
        elif isinstance(other, str):
            return self.num == other[:-1] and self.suit == other[-1]
    
    def __str__(self) -> str:
        return self.num
    
    
    def __repr__(self) -> str:
        return f"{self.num}{self.suit}"


class Deck:
    SUITS = ['♠', '♣', '◆', '❤']
    LETTERS = ['J', 'Q', 'K', 'A']
    def init(self):
        self.deck = []
        self.generate()

    def generate(self):
        for suit in self.SUITS:
            for num in range(2, 11):
                self.deck.append(Card(str(num) + suit))
            for n in range(4):
                self.deck.append(Card(self.LETTERS[n] + suit))
        
        random.shuffle(self.deck)



class Hand:
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8

    def __init__(self, cards: list[Card]):
        self.cards = cards
        self.cards = self.sort_by_value_and_frequency()
        self.cat, self.cat_rank = self.classify()
    
    def __repr__(self):
        return f'Hand({self.cards})'
    
    def __contains__(self, card):
        return card in self.cards
    
    def __gt__(self, other: Hand):
        return self.cat > other.cat
        
    def __eq__(self, other: Hand):
        if isinstance(other, Hand):
            return self.cat == other.cat and self.cat_rank == other.cat_rank
        elif isinstance(other, int):
            return self.cat == other

    def __getitem__(self, index: int):
        return self.cards[index]
    
    def __iter__(self):
        for card in self.cards:
            yield card

    def classify(self):
        
        if self.is_straight_flush():
            return Hand.STRAIGHT_FLUSH, self.get_high_card()
        if self.is_four_of_a_kind():
            return Hand.FOUR_OF_A_KIND, self.get_high_card()
        if self.is_full_house():
            return Hand.FULL_HOUSE, (self.get_high_card(), self[3].num)
        if self.is_flush():
            return Hand.FLUSH, self.get_high_card()
        if self.is_straight():
            return Hand.STRAIGHT, self.get_high_card()
        if self.is_three_of_a_kind():
            return Hand.THREE_OF_A_KIND, self.get_high_card()
        if self.is_two_pair():
            return Hand.TWO_PAIR, (self.get_high_card(), self[2].num)
        if self.is_one_pair():
            return Hand.ONE_PAIR, self.get_high_card()
        
        return Hand.HIGH_CARD, self.get_high_card()


    def get_high_card(self) -> str:
        return self[0].num

    def get_value(self) -> str:
        return self[0].value
    
    def is_four_of_a_kind(self):
        return all(x == self[0] for x in self[:4])

    def is_flush(self):
        def validator(counter: int) -> bool:
            suits = [card.suit for card in self]
            for suit in suits:
                if suits.count(suit) == counter:
                    return True
            return False
        return validator(5)
    
    def is_one_pair(self) -> bool:
        return self[0] == self[1]
    
    def sort_by_value_and_frequency(cards:Card):
        value_counts = {}
        for card in cards:
            if card.value in value_counts:
                value_counts[card.value] += 1
            else:
                value_counts[card.value] = 1

        return sorted(cards, key=lambda card: (value_counts[card.value], card.value), reverse=True)
    
    def is_two_pair(self) -> bool:
        return self[0] == self[1] and self[2] == self[3]
                
    def is_three_of_a_kind(self) -> bool:
        return all(x == self[0] for x in self[:3])

    def is_straight(self) -> bool:
        values = [int(card.value) for card in self]
        buffer = values[0]
        if values[0] == 14 and values[-4] == 5:
            return False
        else:
            for value in values[1:]:
                if buffer - 1 != value:
                    return False
                buffer = value
            return True

    def is_full_house(self) -> bool:
        return all(x == self[0] for x in self[:2]) and self[3] == self[4]
            
    def is_straight_flush(self) -> bool:
        return self.is_straight() and self.is_flush()
