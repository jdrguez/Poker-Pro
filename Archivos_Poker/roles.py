from helpers import combinations
from cards import Card, Hand, Deck


class Dealer:
    def __init__(self, deck):
        self.deck = deck
    
    def deal_to_players(self, players: list):
        for player in players:
            player.recieve_cards([self.deck.draw(), self.deck.draw()])
    
    def deal_community_cards(self) -> list:
        return [self.deck.draw() for _ in range(5)]
    
    def get_best_hand(self, players, community_cards):
        all_cards = Player.private_cards + community_cards
        best_hand = None
        for combo in combinations(all_cards, n=5):
            hand = Hand(list(combo))
            if not best_hand or hand > best_hand:
                best_hand = hand
        return best_hand
    
    def decide_winner(self, player, community_cards):
        pass


class Player:
    def __init__(self, name: str):
        self.name = name
        self.private_cards = []
        self.common_cards = []

    def better_combinations(self, cards: list) -> list:
        return helpers.combinations(cards)
    
    def recieve_cards(self, cards):
        self.private_cards = cards
    
    def best_hand(self, community_cards):
        all_cards = self.private_cards + community_cards
        best_hand = None
        for combo in combinations(all_cards, n=5):
            hand = Hand(list(combo))
            if not best_hand or hand > best_hand:
                best_hand = hand
        return best_hand


