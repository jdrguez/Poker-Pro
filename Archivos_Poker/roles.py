from __future__ import annotations

from cards import Card, Hand
from helpers import combinations


class Dealer:
    def __init__(self, deck: list[str], players: list[Player]):
        self.deck = deck
        self.player1, self.player2 = players

    def revealcards(self, community_cards: list[Card]):
        self.player1.recieve_cmoon_cards(community_cards)
        self.player2.recieve_cmoon_cards(community_cards)

    def deal_private_cards(self, private_cards: list):
        self.player1.recieve_priv_cards(private_cards[0])
        self.player2.recieve_priv_cards(private_cards[1])

    def decide_winner(
        self, players: list[Player], community_cards: list[Card], private_cards: list[Card]
    ):
        player_1, player_2 = players
        self.revealcards(community_cards)
        self.deal_private_cards(private_cards)

        best_hands = player_1.best_hand(), player_2.best_hand()
        best_hand_1, best_hand_2 = best_hands
        if all(card1 == card2 for card1, card2 in zip(best_hand_1, best_hand_2)):
            return None, best_hand_1
        elif best_hand_1 > best_hand_2:
            return player_1, best_hand_1
        elif best_hand_2 > best_hand_1:
            return player_2, best_hand_2
        else:
            for card1, card2 in zip(best_hand_1, best_hand_2):
                if card1 > card2:
                    return player_1, best_hand_1
                elif card2 > card1:
                    return player_2, best_hand_2
            return None, best_hand_1


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
        return self.name

    def best_hand(self):
        all_cards = self.private_cards + self.common_cards
        best_hand = None
        for combo in combinations(all_cards, n=5):
            hand = Hand(list(combo))
            if not best_hand or hand > best_hand:
                best_hand = hand
            elif best_hand == hand:
                for x, y in zip(best_hand, hand):
                    if y > x:
                        best_hand = hand
                        break
                    elif x > y:
                        break
        return best_hand
