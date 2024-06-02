from __future__ import annotations

from cards import Card, Hand
from helpers import combinations


class Dealer:
    def __init__(self, deck: list[str], players: list[Player]):
        """
        Inicializa una instancia de la clase Dealer con el mazo de cartas y los jugadores especificados.

        :param deck: Una lista de cartas que conforman el mazo.
        :type deck: list[str]
        :param players: Una lista de jugadores que participarán en el juego.
        :type players: list[Player]
        """
        self.deck = deck
        self.player1, self.player2 = players

    def revealcards(self, community_cards: list[Card]):
        """
        Revela las cartas comunitarias a los jugadores.

        Este método distribuye las cartas comunitarias a los jugadores para que puedan verlas.

        :param community_cards: Una lista de cartas comunitarias a revelar.
        :type community_cards: list[Card]
        """
        self.player1.recieve_cmoon_cards(community_cards)
        self.player2.recieve_cmoon_cards(community_cards)

    def deal_private_cards(self, private_cards: list):
        """
        Distribuye las cartas privadas a los jugadores.

        Este método asigna las cartas privadas a cada jugador en el juego.

        :param private_cards: Una lista que contiene las cartas privadas de cada jugador.
        :type private_cards: list
        """
        self.player1.recieve_priv_cards(private_cards[0])
        self.player2.recieve_priv_cards(private_cards[1])

    def decide_winner(
        
        self, players: list[Player], community_cards: list[Card], private_cards: list[Card]
    ):
        """
        Decide quién es el ganador del juego.

        Este método determina quién es el ganador del juego basado en las manos de los jugadores y las cartas comunitarias.

        :param players: Una lista que contiene a los jugadores que participan en el juego.
        :type players: list[Player]
        :param community_cards: Una lista de cartas comunitarias en la mesa.
        :type community_cards: list[Card]
        :param private_cards: Una lista de cartas privadas de cada jugador.
        :type private_cards: list[Card]
        :return: Una tupla que contiene al jugador ganador y su mejor mano, o None si hay un empate.
        :rtype: tuple(Player, list[Card]) or tuple(None, list[Card])
        """
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
        """
        Inicializa una instancia de la clase Jugador con el nombre especificado.

        :param name: El nombre del jugador.
        :type name: str
        """
        self.name = name
        self.private_cards = []
        self.common_cards = []

    def recieve_priv_cards(self, cards: list[Card]):
        """
        Recibe las cartas privadas del jugador.

        Este método asigna las cartas privadas recibidas al jugador.

        :param cards: Una lista de cartas privadas recibidas.
        :type cards: list[Card]
        """
        self.private_cards = cards

    def recieve_cmoon_cards(self, cards: list[Card]):
        """
        Recibe las cartas comunitarias del jugador.

        Este método asigna las cartas comunitarias recibidas al jugador.

        :param cards: Una lista de cartas comunitarias recibidas.
        :type cards: list[Card]
        """
        self.common_cards = cards

    def __str__(self):
        """
        Devuelve una representación en forma de cadena del jugador.

        :return: El nombre del jugador como una cadena.
        :rtype: str
        """
        return self.name

    def best_hand(self):
        """
        Determina la mejor mano posible para el jugador.

        Este método genera todas las combinaciones posibles de cinco cartas entre las cartas privadas y comunitarias
        del jugador, y determina la mejor mano posible entre esas combinaciones.

        :return: La mejor mano posible para el jugador.
        :rtype: Hand
        """
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
