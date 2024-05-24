from helpers import shuffle, combinations



class Card:
    def __init__(self, card:str):
        self.card = card
        self.value = card[0]
        self.suit = card[1]
    pass

    def __repr__(self) -> str:
        return f"{self.value}{self.suit}"


class Deck:
    pass


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

    def __init__(self, cards: list):
        self.cards = cards
        self.cat = None
        self.cat_rank = None
        self.evaluate_hand()
    
    def evaluate_hand(self):
        pass
    
    def __contains__(self, card):
        return card in self.cards
    
    ## No se si es la mejor manera o será con atributos
    @classmethod
    def get_high_card() -> str:
        pass
    
    @classmethod
    def get_one_pair() -> str:
        pass
    
    @classmethod
    def get_two_pair() -> str:
        pass
    
    @classmethod
    def get_three_of_a_kind() -> str:
        pass
    
    @classmethod
    def get_straight() -> str:
        pass
    
    @classmethod
    def get_flush() -> str:
        pass

    @classmethod
    def get_full_house() -> str:
        pass
    
    @classmethod
    def get_four_of_a_kind() -> str:
        pass
    
    @classmethod
    def get_straight_flush() -> str:
        pass



    def __contains__(self) -> bool:
        return self in self.cards
    pass