# Revisar este código
from cards import Deck
from roles import Dealer


class Game:
    def __init__(self, players):
        """
        Inicializa una instancia de la clase Juego de Cartas con los jugadores especificados.

        :param players: Una lista de jugadores que participarán en el juego.
        :type players: list
        """
        self.player = players
        self.deck = Deck()
        self.dealer = Dealer(self.deck, players)


def get_winner(players, community_cards, private_cards):
    """
    Obtiene al ganador de una partida de póker.

    :param players: Una lista de jugadores que participan en la partida.
    :type players: list
    :param community_cards: Una lista de cartas comunitarias en la mesa.
    :type community_cards: list
    :param private_cards: Una lista de cartas privadas de los jugadores.
    :type private_cards: list
    :return: El jugador que gana la partida.
    :rtype: Player
    """
    deck = Deck()
    dealer = Dealer(deck, players)

    return dealer.decide_winner(players, community_cards, private_cards)
