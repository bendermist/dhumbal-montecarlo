from game import Game

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.called_dhumbal = False

    def draw_card(self, cards):
        # Draw a card from the deck and add it to the player's hand
        if cards:
            self.hand.append(cards.pop())
            print(self.name, "drew card", self.hand[-1])

    def play_cards(self, cards_to_play, game: Game):
        # Play multiple cards from the player's hand
        # This method assumes that cards_to_play is a list of Card objects
        for card in cards_to_play:
            if card in self.hand:
                self.hand.remove(card)
                game.graveyard.append(card)
            else:
                raise ValueError("Card not in hand")
        print(self.name, "played cards", [str(card) for card in cards_to_play])

    def show_hand(self):
        # Display the player's current hand
        return self.hand

    def has_valid_play(self, cards_to_play):
        # Check if the cards to play are either of the same value or a valid straight flush
        if self.is_same_value(cards_to_play) or self.is_straight_flush(cards_to_play):
            return True
        return False

    @staticmethod
    def is_same_value(cards):
        # Check if all cards are of the same value
        if len(set(card.rank for card in cards)) == 1:
            return True
        return False

    @staticmethod
    def is_straight_flush(cards):
        # Check if the cards form a straight flush (three or more cards in sequence of the same suit)
        if len(cards) < 3:
            return False

        # Sort cards by rank
        sorted_cards = sorted(cards, key=lambda card: card.rank.value)
        suit = sorted_cards[0].suit

        for i in range(len(sorted_cards) - 1):
            if sorted_cards[i+1].rank.value - sorted_cards[i].rank.value != 1 or sorted_cards[i].suit != suit:
                return False

        return True

    def calculate_score(self):
        total_score = 0
        for card in self.hand:
            # Add the card's value to the total score
            total_score += card.rank.value

            # Handle any special rules for Jokers or other special cards
            # For example, if Jokers have a special value or rule, add that logic here

        return total_score

    def make_a_move(self, game: Game):
        # Decide the next action based on the game state
        # This function can be expanded based on how the game state is defined
        if self.calculate_score() <= 5:
            self.called_dhumbal = True
            print(self.name, "called Dhumbal")
            return True
        self.play_cards([self.hand[0]], game)
        self.draw_card(game.deck.cards)
    
        return False
        
    