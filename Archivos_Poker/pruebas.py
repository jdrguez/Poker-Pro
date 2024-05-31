from __future__ import annotations

from helpers import combinations, random, shuffle


class Card:
    VALUES = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    def __init__(self, card):
        self.suit = card[-1]
        self.num = card[0:-1]
        self.value = self.VALUES[self.num] if self.num in self.VALUES else int(self.num)

    def __gt__(self, other: Card) -> bool:
        return self.value > other.value

    def __eq__(self, other: Card) -> bool:
        return self.value == other.value

    def __str__(self) -> str:
        return f'{self.num}{self.suit}'

    def __repr__(self) -> str:
        return f"{self.num}{self.suit}"


class Deck:
    SUITS = ['♠', '♣', '◆', '❤']
    LETTERS = ['J', 'Q', 'K', 'A']

    def __init__(self):
        self.deck = []
        self.generate()

    def generate(self):
        for suit in self.SUITS:
            for num in range(2, 11):
                self.deck.append(Card(str(num) + suit))
            for n in range(4):
                self.deck.append(Card(self.LETTERS[n] + suit))

        random.shuffle(self.deck)

    def pop(self):
        if self.deck:
            return self.deck.pop()
        return None


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
        self.cards = cards
        self.cards = self.sort_by_value_and_frequency()
        self.cat, self.cat_rank = self.classify()

    def __repr__(self):
        return f'Hand({self.cards})'

    def __contains__(self, card):
        return card in self.cards

    def __gt__(self, other: Hand):
        return self.cat > other.cat

    def __eq__(self, other: Hand):
        return self.cat == other.cat

    def __getitem__(self, index: int):
        return self.cards[index]

    def __iter__(self):
        for card in self.cards:
            yield card

    def classify(self):

        if self.is_straight_flush():
            return Hand.STRAIGHT_FLUSH, self.get_high_card()
        elif self.is_four_of_a_kind():
            return Hand.FOUR_OF_A_KIND, self.get_high_card()
        elif self.is_full_house():
            return Hand.FULL_HOUSE, (self.get_high_card(), self[3])
        elif self.is_flush():
            return Hand.FLUSH, self.get_high_card()
        elif self.is_straight():
            return Hand.STRAIGHT, self.get_high_card()
        elif self.is_three_of_a_kind():
            return Hand.THREE_OF_A_KIND, self.get_high_card()
        elif self.is_two_pair():
            return Hand.TWO_PAIR, (self.get_high_card(), self[2])
        elif self.is_one_pair():
            return Hand.ONE_PAIR, self.get_high_card()

        return Hand.HIGH_CARD, self.get_high_card()

    def get_high_card(self) -> bool:
        return self[0]

    def is_four_of_a_kind(self):
        return (
            self[0] == self[1] and self[0] == self[2] and self[0] == self[3] and self[0] == self[4]
        )

    def is_flush(self):
        def validator(counter: int) -> bool:
            suits = [card.suit for card in self]
            for suit in suits:
                if suits.count(suit) == counter:
                    return True
            return False

        return validator(5)

    def is_one_pair(self) -> bool:
        return self[0] == self[1]

    def sort_by_value_and_frequency(cards):
        value_counts = {}
        for card in cards:
            if card.value in value_counts:
                value_counts[card.value] += 1
            else:
                value_counts[card.value] = 1

        return sorted(cards, key=lambda card: (value_counts[card.value], card.value), reverse=True)

    def is_two_pair(self) -> bool:
        return self[0] == self[1] and self[2] == self[3]

    def is_three_of_a_kind(self) -> bool:
        return all(x == self[0] for x in self[:3])

    def is_straight(self) -> bool:
        values = [int(card.value) for card in self]
        buffer = values[0]
        for value in values[1:]:
            if buffer - 1 != value:
                return False
            buffer = value
        return True

    def is_full_house(self) -> bool:
        return all(x == self[0] for x in self[:3]) and self[3] == self[4]

    def is_straight_flush(self) -> bool:
        return self.is_straight() and self.is_flush()


class Dealer:
    def __init__(self, deck: list[str], player1: Player, player2: Player):
        self.deck = deck
        self.player1 = player1
        self.player2 = player2

    def __getitem__(self, index: int):
        return self.deck[index]

    def deal_cards(self, num_cards: int) -> list:
        return [self.deck.pop() for _ in range(num_cards)]

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

    def __gt__(self, other: Player):
        return self.best_hand() > other.best_hand()

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
        return best_hand

    def winner(self):
        if player1 > player2:
            return player1.name
        return player2.name


if __name__ == '__main__':

    deck = Deck()

    print(deck.deck)
    player1 = Player('player1')
    print(player1)
    player2 = Player('player2')
    print(player2)

    common = [Card('A◆'), Card('7❤'), Card('7♣'), Card('2❤'), Card('2♠')]

    player1.recieve_cmoon_cards(common)
    player2.recieve_cmoon_cards(common)

    player1.recieve_priv_cards([Card('Q♣'), Card('9◆')])
    player2.recieve_priv_cards([Card('10❤'), Card('5❤')])

    print(f'Player2 {player2.private_cards}')
    print(player1.best_hand())
    print(player2.best_hand())

    print(player1.best_hand().cat)

    print(f'Ganador: {player1.winner()}')
