from __future__ import annotations

from helpers import random


class Card:
    VALUES = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    def __init__(self, card: str):
        """
        Inicializa una instancia de la clase con una carta específica.

        :param card: Una cadena que representa una carta. La última letra 
                    representa el palo (suit) y el resto de la cadena 
                    representa el valor numérico (num).
        :type card: str

        :ivar suit: El palo de la carta.
        :vartype suit: str
        :ivar num: El valor numérico de la carta en forma de cadena.
        :vartype num: str
        :ivar value: El valor de la carta. Se obtiene de la constante 
                    VALUES si el valor está presente en ella; de lo 
                    contrario, se convierte a entero.
        :vartype value: int
        """
        self.suit = card[-1]
        self.num = card[0:-1]
        self.value = self.VALUES[self.num] if self.num in self.VALUES else int(self.num)


    def __gt__(self, other: Card) -> bool:
        """
        Compara si el valor de esta carta es mayor que el valor de otra carta.

        :param other: La otra carta con la que se va a comparar.
        :type other: Card
        :return: True si el valor de esta carta es mayor que el valor de la otra carta, False en caso contrario.
        :rtype: bool
        """
        return self.value > other.value

    def __eq__(self, other: Card) -> bool:
        """
        Compara si esta carta es igual a otra carta o a una cadena que representa una carta.

        :param other: La otra carta o cadena con la que se va a comparar. Puede ser una instancia de la clase Card o una cadena.
        :type other: Card or str
        :return: True si las cartas son iguales, False en caso contrario.
        :rtype: bool
        """
        if isinstance(other, Card):
            return self.num == other.num
        elif isinstance(other, str):
            return self.num == other[:-1] and self.suit == other[-1]

    def __str__(self) -> str:
        """
        Devuelve una representación en forma de cadena del valor numérico de la carta.

        :return: El valor numérico de la carta.
        :rtype: str
        """
        return self.num

    def __repr__(self) -> str:
        """
        Devuelve una representación oficial en forma de cadena de la carta.

        :return: Una cadena que representa la carta en el formato "num" + "suit".
        :rtype: str
        """
        return f"{self.num}{self.suit}"


class Deck:
    SUITS = ['♠', '♣', '◆', '❤']
    LETTERS = ['J', 'Q', 'K', 'A']

    def init(self):
        """
        Inicializa la baraja de cartas y genera el mazo completo.

        :ivar deck: La lista que contiene las cartas de la baraja.
        :vartype deck: list
        """
        self.deck = []
        self.generate()

    def generate(self):
        """
        Genera una baraja completa de cartas y las baraja.

        Este método llena la baraja con cartas de los palos definidos en `SUITS`.
        Para cada palo, agrega cartas numéricas del 2 al 10 y cartas de letras 
        (generalmente J, Q, K, A). Luego, la baraja es mezclada aleatoriamente.

        :ivar deck: La lista que contiene las cartas generadas y barajadas.
        :vartype deck: list
        """
        for suit in self.SUITS:
            for num in range(2, 11):
                self.deck.append(Card(str(num) + suit))
            for n in range(4):
                self.deck.append(Card(self.LETTERS[n] + suit))

        random.shuffle(self.deck)


class Hand:
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8

    def __init__(self, cards: list[Card]):
        """
        Inicializa una instancia de la clase con una lista de cartas.

        :param cards: Una lista de cartas.
        :type cards: list[Card]

        :ivar cards: La lista de cartas que conforman la mano.
        :vartype cards: list[Card]
        :ivar cat: La categoría de la mano (por ejemplo, "Poker", "Full House", "Flush", etc.).
        :vartype cat: str
        :ivar cat_rank: La clasificación de la mano dentro de su categoría.
        :vartype cat_rank: int
        """
        self.cards = cards
        self.cards = self.sort_by_value_and_frequency()
        self.cat, self.cat_rank = self.classify()

    def __repr__(self):
        """
        Devuelve una representación oficial en forma de cadena de la mano.

        :return: Una cadena que representa la instancia de la mano en el formato "Hand(cards)".
        :rtype: str
        """
        return f'Hand({self})'

    def __contains__(self, card):
        """
        Comprueba si una carta está presente en la mano.

        :param card: La carta que se va a buscar en la mano.
        :type card: Card
        :return: True si la carta está en la mano, False en caso contrario.
        :rtype: bool
        """
        return card in self.cards

    def __gt__(self, other: Hand):
        """
        Compara si esta mano es mayor que otra mano.

        :param other: La otra mano con la que se va a comparar.
        :type other: Hand
        :return: True si esta mano es mayor que la otra mano, False en caso contrario.
        :rtype: bool
        """
        if self.cat == other.cat:
            best_value1 = self.get_value()
            best_value2 = other.get_value()
            return best_value1 > best_value2
        return self.cat > other.cat

    def __eq__(self, other: Hand):
        """
        Compara si esta mano es igual a otra mano o a un entero que representa la categoría de una mano.

        :param other: La otra mano o un entero que representa la categoría de una mano con la que se va a comparar.
        :type other: Hand or int
        :return: True si las manos son iguales o si la categoría de esta mano coincide con el entero proporcionado, False en caso contrario.
        :rtype: bool
        """
        if isinstance(other, Hand):
            return self.cat == other.cat
        elif isinstance(other, int):
            return self.cat == other

    def __getitem__(self, index: int):
        """
        Obtiene una carta específica de la mano mediante su índice.

        :param index: El índice de la carta que se va a obtener.
        :type index: int
        :return: La carta en la posición especificada.
        :rtype: Card
        """
        return self.cards[index]

    def __add__(self, other: Hand):
        """
        Concatena dos manos y devuelve una nueva lista de cartas que contiene todas las cartas de ambas manos.

        :param other: La otra mano que se va a concatenar.
        :type other: Hand
        :return: Una lista que contiene todas las cartas de esta mano y la otra mano.
        :rtype: list[Card]
        """
        return self.cards.extend(other.cards)

    def __iter__(self):
        """
        Itera sobre las cartas de la mano.

        Este método permite iterar sobre las cartas de la mano utilizando un bucle for.

        :yield: Cada carta de la mano.
        :rtype: Card
        """
        for card in self.cards:
            yield card

    def classify(self):
        """
        Clasifica la mano de acuerdo con las reglas del póker.

        Este método clasifica la mano de acuerdo con las reglas del póker y devuelve una tupla que contiene
        la categoría de la mano y, en algunos casos, información adicional sobre la clasificación.

        :return: Una tupla que contiene la categoría de la mano y, en algunos casos, información adicional sobre la clasificación.
        :rtype: tuple
        """
        if self.is_straight_flush():
            return Hand.STRAIGHT_FLUSH, self.get_high_card()
        if self.is_four_of_a_kind():
            return Hand.FOUR_OF_A_KIND, self.get_high_card()
        if self.is_full_house():
            return Hand.FULL_HOUSE, (self.get_high_card(), self[3].num)
        if self.is_flush():
            return Hand.FLUSH, self.get_high_card()
        if self.is_straight():
            return Hand.STRAIGHT, self.get_high_card()
        if self.is_three_of_a_kind():
            return Hand.THREE_OF_A_KIND, self.get_high_card()
        if self.is_two_pair():
            return Hand.TWO_PAIR, (self.get_high_card(), self[2].num)
        if self.is_one_pair():
            return Hand.ONE_PAIR, self.get_high_card()

        return Hand.HIGH_CARD, self.get_high_card()

    def get_high_card(self) -> str:
        """
        Obtiene la carta de mayor valor en la mano.

        :return: El valor numérico de la carta de mayor valor en la mano.
        :rtype: str
        """
        return self[0].num

    def get_value(self) -> str:
        """
        Obtiene el valor de la mano.

        :return: El valor de la mano, que generalmente corresponde al valor de la carta de mayor valor en la mano.
        :rtype: str
        """
        return self[0].value

    def is_four_of_a_kind(self):
        """
        Verifica si la mano contiene cuatro cartas del mismo valor.

        :return: True si la mano contiene cuatro cartas del mismo valor, False en caso contrario.
        :rtype: bool
        """
        return all(x == self[0] for x in self[:4])

    def is_flush(self):
        """
        Verifica si la mano contiene un flush, es decir, todas las cartas tienen el mismo palo.

        :return: True si la mano contiene un flush, False en caso contrario.
        :rtype: bool
        """
        def validator(counter: int) -> bool:
            suits = [card.suit for card in self]
            for suit in suits:
                if suits.count(suit) == counter:
                    return True
            return False

        return validator(5)

    def is_one_pair(self) -> bool:
        """
        Verifica si la mano contiene una pareja de cartas del mismo valor.

        :return: True si la mano contiene una pareja de cartas del mismo valor, False en caso contrario.
        :rtype: bool
        """
        return self[0] == self[1]

    def sort_by_value_and_frequency(self):
        """
        Ordena las cartas de la mano primero por su valor y luego por la frecuencia de aparición de ese valor.

        Este método calcula la frecuencia de aparición de cada valor de carta en la mano y luego ordena las cartas
        primero por su frecuencia de aparición y luego por su valor, en orden descendente.

        :return: Una lista de cartas ordenadas.
        :rtype: list[Card]
        """
        value_counts = {}
        for card in self:
            if card.value in value_counts:
                value_counts[card.value] += 1
            else:
                value_counts[card.value] = 1

        return sorted(self, key=lambda card: (value_counts[card.value], card.value), reverse=True)

    def is_two_pair(self) -> bool:
        """
        Verifica si la mano contiene dos parejas de cartas del mismo valor.

        :return: True si la mano contiene dos parejas de cartas del mismo valor, False en caso contrario.
        :rtype: bool
        """
        return self[0] == self[1] and self[2] == self[3]

    def is_three_of_a_kind(self) -> bool:
        """
        Verifica si la mano contiene tres cartas del mismo valor.

        :return: True si la mano contiene tres cartas del mismo valor, False en caso contrario.
        :rtype: bool
        """
        return all(x == self[0] for x in self[:3])

    def is_straight(self) -> bool:
        """
        Verifica si la mano contiene una escalera, es decir, todas las cartas tienen valores consecutivos.

        :return: True si la mano contiene una escalera, False en caso contrario.
        :rtype: bool
        """
        values = [int(card.value) for card in self]
        buffer = values[0]
        if values[0] == 14 and values[-4] == 5:
            return False
        else:
            for value in values[1:]:
                if buffer - 1 != value:
                    return False
                buffer = value
            return True

    def is_full_house(self) -> bool:
        """
        Verifica si la mano contiene un full house, es decir, tres cartas del mismo valor y dos cartas del mismo valor.

        :return: True si la mano contiene un full house, False en caso contrario.
        :rtype: bool
        """
        return all(x == self[0] for x in self[:2]) and self[3] == self[4]

    def is_straight_flush(self) -> bool:
        """
        Verifica si la mano contiene un full house, es decir, tres cartas del mismo valor y dos cartas del mismo valor.

        :return: True si la mano contiene un full house, False en caso contrario.
        :rtype: bool
        """
        return self.is_straight() and self.is_flush()
