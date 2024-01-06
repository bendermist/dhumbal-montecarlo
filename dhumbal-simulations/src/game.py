from cards import Deck
from scoreboard import Scoreboard

class Game:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()
        self.graveyard = []
        self.current_player = self.players[0]
        self.turn = 0
        self.round = 0
        self.round_over = False
        self.game_over = False
        self.scoreboard = Scoreboard(self.players)

    def start_game(self):
        self.deck.shuffle_deck()
        while not self.game_over:
            self.deal_cards()
            self.play_round()
            self.record_scores()
            self.remove_eliminated_players()
            if self.check_game_end():
                self.game_over = True
            else:
                self.prepare_next_round()
        print("Game Over", self.scoreboard.get_scores())

    def deal_cards(self):
        for _ in range(5):
            for player in self.players:
                player.draw_card(self.deck.cards, self)
        self.graveyard.append(self.deck.cards.pop())
    
    def check_refill_deck(self):
        if not self.deck.cards:
            self.deck.cards = self.graveyard[:-1]
            self.graveyard = self.graveyard[-1:]
            print("Deck refilled")

    def play_round(self):
        # Determine the starting index of the current player
        start_index = self.players.index(self.current_player)

        # Loop until the round is over
        while not self.round_over:
            for i in range(len(self.players)):
                # Calculate the current player's index
                current_index = (start_index + i + 1) % len(self.players)
                player = self.players[current_index]

                if player.make_a_move(self):
                    # If player calls "Dhumbal", end the round
                    self.round_over = True
                    break
                self.check_refill_deck()

            self.turn += 1
            print("Turn", self.turn)
            if self.turn > 100:
                print("Turn limit (100) reached. Code breaking")
                self.game_over = True
                break

    def record_scores(self):
        # Calculate and record scores at the end of the round
        self.scoreboard.record_round(self)

    def remove_eliminated_players(self):
        # Remove players with 108 points or more
        eliminated_players = self.scoreboard.get_eliminated_players()
        self.players = [player for player in self.players if player not in eliminated_players]

    def check_game_end(self):
        # Game ends if 1 or fewer players remain with less than 108 points
        return len(self.players) <= 1

    def prepare_next_round(self):
        # Reset the deck and graveyard for the next round
        self.deck = Deck()
        self.deck.shuffle_deck()
        self.graveyard.clear()
        self.turn = 0
        self.round += 1
        self.round_over = False
        self.current_player = self.scoreboard.get_last_player()
        for player in self.players:
            player.hand.clear()
            player.called_dhumbal = False
        print("Starting Round", self.round)
        print("Current Scores:", self.scoreboard.get_scores())    
        # input("Press Enter to continue...")
        

    # Other methods like next_player, current_player, draw_card, etc. remain the same
