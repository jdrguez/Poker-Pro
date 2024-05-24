# Revisar este código
from roles import Player
from cards import Card, Hand



def get_winner(players, community_cards, private_cards):
    best_hands = []
    for player, priv_cards in zip(players, private_cards):
        hand = player.best_hand(community_cards + priv_cards)
        best_hands.append((player, hand))

    best_hands.sort(key=lambda x: x[1], reverse=True)
    winning_hand = best_hands[0][1]

    winners = [player for player, hand in best_hands if hand == winning_hand]

    if len(winners) > 1:
        return None, winning_hand  
    return winners[0], winning_hand
