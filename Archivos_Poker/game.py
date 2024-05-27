# Revisar este código
from roles import Player
from cards import Card, Hand


class Game:
    def __init__(self, players):
        self.player = players
        self.dealer = Dealer()
        self.deck = Deck()



def get_winner(players, community_cards, private_cards):
    best_hands = []
    player_1, player_2 = players

    player_1.recieve_priv_cards(private_cards[0])
    player_1.recieve_cmoon_cards(community_cards)
    player_2.recieve_priv_cards(private_cards[1])
    player_2.recieve_cmoon_cards(community_cards)
    best_hands.append(player_1.best_hand())
    best_hands.append(player_2.best_hand())

    winner = max(best_hands)

    return player_1, winner
    




