from helpers import combinations



class Dealer:
    pass


class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards = []
        self.common_cards = []

    def better_combinations(self, cards: list) -> list:
        return helpers.combinations(cards)
    pass



