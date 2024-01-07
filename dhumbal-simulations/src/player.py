from abc import ABC, abstractmethod
from game import Game

class PlayerStrategy(ABC):
    @abstractmethod
    def make_a_move(self, player, game):
        pass

    def get_cards_with_same_rank(self, player, card):
        # Returns a list of cards from the player's hand that have the same rank as the first card in their hand
        return [c for c in player.hand if c.rank.name == card.rank.name]

class MinimizeCardNumberStrategy(PlayerStrategy):
    def __init__(self, dhumbal_threshold, draw_graveyard_threshold, try_to_pool_threshold, verbose=False):
        # Initialize the strategy with two thresholds:
        # dhumbal_threshold: The score threshold below which the player will call Dhumbal
        # draw_graveyard_threshold: The card rank threshold to decide whether to draw from the graveyard or the deck
        self.dhumbal_threshold = dhumbal_threshold
        self.draw_graveyard_threshold = draw_graveyard_threshold
        self.try_to_pool_threshold = try_to_pool_threshold
        self.verbose = verbose

    def make_a_move(self, player, game: Game):
        # This function defines the player's move based on the current game state
        
        # Check if the player's score is low enough to call Dhumbal
        if player.calculate_score() <= self.dhumbal_threshold:
            player.called_dhumbal = True
            print(player.name, f"called Dhumbal, as have {player.calculate_score()}") if self.verbose else None
            return True  # End the turn after calling Dhumbal
        
        # Find the card with the highest rank in the player's hand
        highest_rank_card = max(player.hand, key=lambda card: card.rank.value)

        # Check if the top card in the graveyard has the same rank with any of cards in hand
        # yet within the threshold defined by try_to_pool_threshold
        if (
                game.graveyard[-1].rank.name in [card.rank.name for card in player.hand] and 
                game.graveyard[-1].rank.value >= self.try_to_pool_threshold 
            ):
            # If so, find the second highest rank card in hand other than the top card in the graveyard
            filtered_cards = [card for card in player.hand if card.rank.name != game.graveyard[-1].rank.name]
            if len(filtered_cards) > 0:        
                filtered_highest_rank_card = max(
                    filtered_cards, 
                    key=lambda card: card.rank.value
                )
                # Play cards with the same rank as the filtered highest card
                player.play_cards(self.get_cards_with_same_rank(player, filtered_highest_rank_card))
                player.draw_card(game.graveyard, game)
                print(player.name, "drew card from graveyard, as want to pair") if self.verbose else None
                return False  # Continue the game

        # If not, play cards with the same rank as the highest card
        player.play_cards(self.get_cards_with_same_rank(player, highest_rank_card))
        
        # Decide whether to draw a card from the graveyard or the deck
        threshold_to_draw_from_graveyard = self.draw_graveyard_threshold - max(4, game.turn // 4)
        if game.graveyard[-1].rank.value <= threshold_to_draw_from_graveyard:
            # Draw from the graveyard if the top card's rank is above the threshold
            player.draw_card(game.graveyard, game)
            print(player.name, f"drew card from graveyard, as less than {threshold_to_draw_from_graveyard}") if self.verbose else None
        else:
            # Otherwise, draw from the deck
            player.draw_card(game.deck.cards, game)
            print(player.name, "drew card from deck, as graveyard high") if self.verbose else None
    
        return False  # Continue the game



class DiscardBiggestStrategy(PlayerStrategy):
    def __init__(self, dhumbal_threshold, draw_graveyard_threshold):
        self.dhumbal_threshold = dhumbal_threshold
        self.draw_graveyard_threshold = draw_graveyard_threshold
    def make_a_move(self, player, game: Game):
        # Decide the next action based on the game state
        # This function can be expanded based on how the game state is defined
        if player.calculate_score() <= self.dhumbal_threshold:
            player.called_dhumbal = True
            print(player.name, f"called Dhumbal, as have {player.calculate_score()}") if self.verbose else None
            return True
        
        highest_rank_card = max(player.hand, key=lambda card: card.rank.value)
        
        player.play_cards(self.get_cards_with_same_rank(player, highest_rank_card))
        
        threshold_to_draw_from_graveyard = self.draw_graveyard_threshold - max(4, game.turn // 4)        
        if game.graveyard[-1].rank.value <= threshold_to_draw_from_graveyard:
            player.draw_card(game.graveyard, game)
            print(player.name, f"drew card from graveyard, as less than {threshold_to_draw_from_graveyard}") if self.verbose else None
        else:
            player.draw_card(game.deck.cards, game)
            print(player.name, "drew card from deck, as grave bad") if self.verbose else None
    
        return False


class Player:
    def __init__(self, name, strategy: PlayerStrategy, verbose=False):
        self.name = name
        self.strategy = strategy
        self.verbose = verbose
        self.strategy.verbose = verbose
        self.hand = []
        self.called_dhumbal = False
        self.cards_to_be_played = []

    def draw_card(self, cards, game: Game):
        # Draw a card from the deck and add it to the player's hand
        if cards:
            self.hand.append(cards.pop())
            print(self.name, "drew card", self.hand[-1]) if self.verbose else None
        game.graveyard.extend(self.cards_to_be_played)
        self.cards_to_be_played.clear()

    def play_cards(self, cards_to_play):
        # Play multiple cards from the player's hand
        # This method assumes that cards_to_play is a list of Card objects
        for card in cards_to_play:
            if card in self.hand:
                self.hand.remove(card)
                self.cards_to_be_played.append(card)
            else:
                raise ValueError("Card not in hand")
        print(self.name, "played cards", [str(card) for card in cards_to_play]) if self.verbose else None

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
            total_score += min(card.rank.value,10)

            # Handle any special rules for Jokers or other special cards
            # For example, if Jokers have a special value or rule, add that logic here

        return total_score

    def make_a_move(self, game: Game):
        return self.strategy.make_a_move(self, game)
        
    