from __future__ import annotations
from helpers import combinations
from cards import Card, Hand, Deck



class Dealer:
    def __init__(self, deck: list[str], players: Player):
        self.deck = deck
        self.player1, self.player2 = players

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
    
    def decide_winner(self, players: Player, community_cards:list[Card], private_cards:list[Card]):
        player_1, player_2 = players
        player_1.recieve_priv_cards(private_cards[0])
        player_1.recieve_cmoon_cards(community_cards)
        player_2.recieve_priv_cards(private_cards[1])
        player_2.recieve_cmoon_cards(community_cards)
        
        best_hands = player_1.best_hand(), player_2.best_hand()
        best_hand_1, best_hand_2 = best_hands
        
        print(best_hand_1)
        print(best_hand_2)
        
        print(best_hand_1.cat)
        
        print(best_hand_1.cat_rank)
        print(best_hand_2.cat_rank)
        
        
        
        if best_hand_1 > best_hand_2:
            return player_1, best_hand_1
        elif best_hand_2 > best_hand_1:
            return player_2, best_hand_2
        else:
            if all(card1 == card2 for card1, card2 in zip(best_hand_1, best_hand_2)):
                return None, best_hand_1
            elif best_hand_1.cat == best_hand_2.cat:                    
                best_value1 = best_hand_1.get_value()
                best_value2 = best_hand_2.get_value()
                if best_hand_1.cat == Hand.STRAIGHT and best_value1 == best_value2:
                    return None, best_hand_1
                elif best_value1 > best_value2:
                    return player_1, best_hand_1
                elif best_value2 > best_value1:
                    return player_2, best_hand_2
                
                else:
                    if best_hand_1.cat == Hand.TWO_PAIR and best_hand_2 == Hand.TWO_PAIR:
                        best_value1 = best_hand_1.cat_rank[1] 
                        best_value2 = best_hand_2.cat_rank[1] 
                        
                        best_value1 = Card.VALUES[best_value1] if best_value1 in Card.VALUES else int(best_value1)
                        best_value2 = Card.VALUES[best_value2] if best_value2 in Card.VALUES else int(best_value2)
                        
                        print(best_value1)
                        print(best_value2)
                        if best_value1 > best_value2:
                            return player_1, best_hand_1
                        elif best_value2 > best_value1:
                            return player_2, best_hand_2
                        else:
                            max_card_1 = max(player_1.private_cards)
                            max_card_2 = max(player_2.private_cards)
                            if max_card_1 > max_card_2:
                                return player_1, best_hand_1
                            elif max_card_1 < max_card_2:
                                return player_2, best_hand_2
                            else:
                                for card1, card2 in zip(best_hand_1, best_hand_2):
                                    if card1 > card2:
                                        return player_1, best_hand_1
                                    elif card2 > card1:
                                        return player_2, best_hand_2
                                return None, best_hand_1
                    else:
                        max_card_1 = max(player_1.private_cards)
                        max_card_2 = max(player_2.private_cards)
                        
                        if max_card_1 > max_card_2:
                            return player_1, best_hand_1
                        elif max_card_1 < max_card_2:
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
    


