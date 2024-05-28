# Revisar este código
from roles import Player, Dealer
from cards import Card, Hand, Deck


class Game:
    def __init__(self, players):
        self.player = players
        self.deck = Deck()
        self.dealer = Dealer(self.deck, players)



def get_winner(players, community_cards, private_cards):
    deck = Deck()
    dealer =  Dealer(deck, players)
    
    return dealer.decide_winner(players, community_cards, private_cards)
    
    
    




