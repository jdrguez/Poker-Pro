from __future__ import annotations
from helpers import combinations
from cards import Card, Hand, Deck



class Dealer:
    def init(self, deck: list[str], player1: Player, player2: Player):
        self.deck = deck
        self.player1 = player1
        self.player2 = player2

    def deal_cards(self, num_cards: int) -> list:
        return [self.deck.pop(0) for _ in range(num_cards)]

    def revealcards(self) -> list[str]:
        community_cards = self.deal_cards(5)
        self.player1.recieve_cmoon_cards(community_cards)
        self.player2.recieve_cmoon_cards(community_cards)
        return community_cards

    def deal_private_cards(self):
        self.player1.recieve_priv_cards(self.deal_cards(2))
        self.player2.recieve_priv_cards(self.deal_cards(2))

    def best_hands(self) -> tuple[str, list[str]]:
        hand1 = self.player1.best_hand()
        hand2 = self.player2.best_hand()

        if hand1 > hand2:
            return (self.player1.name, hand1)
        else:
            return (self.player2.name, hand2)
    
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
    
    def recieve_priv_cards(self, cards: list[Card]):
        self.private_cards = cards
    
    def recieve_cmoon_cards(self, cards: list[Card]):
        self.common_cards = cards
        
    def __str__(self):
        return name
    
    def best_hand(self):
        all_cards = self.private_cards + self.common_cards
        best_hand = None
        for combo in combinations(all_cards, n=5):
            hand = Hand(list(combo))
            if not best_hand or hand > best_hand:
                best_hand = hand
        return best_hand


