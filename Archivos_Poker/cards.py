from helpers import combinations



class Card:
    def __init__(self, card:str):
        self.card = card
        self.value = card[0]
        self.suit = card[1]
    pass



class Deck:
    pass


class Hand:

    def __init__(self, cards: list):
        self.cards = cards
    
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