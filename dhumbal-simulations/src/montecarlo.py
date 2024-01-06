from collections import defaultdict
import matplotlib.pyplot as plt

from cards import Deck
from game import Game
from player import Player, DiscardBiggestStrategy, MinimizeCardNumberStrategy


class MonteCarlo:
    def __init__(self, players, num_simulations):
        self.num_simulations = num_simulations
        self.players = players
        self.game = Game(self.players) # Game object used to run simulations
        
    def run_simulation(self):
        results = []
        for _ in range(self.num_simulations):
            self.game = Game(self.players)  # Reset the game
            self.game.start_game()
            results.append(self.game.scoreboard.round_log)
        self.results = results

    def analyze_results(self):
        player_wins = defaultdict(int)
        completed_games = [result for result in self.results if len(result) > 0]
        print(len(self.results)-len(completed_games),"out of", len(self.results), "games ended in a draw")
        for simulation in completed_games:
            last_round = simulation[-1]
            # Sort players based on score_total, score_at_round, and Result.value
            sorted_players = sorted(
                last_round.items(), 
                key=lambda x: (x[1][1], x[1][0], x[1][2].value)
            )
            winner = sorted_players[0][0]  # Player with the lowest combined score
            player_wins[winner] += 1

        # Calculate win percentages
        win_percentages = {player.name: wins / len(completed_games) * 100 for player, wins in player_wins.items()}

        return win_percentages

    def visualize_data(self, data):
        
        players = list(data.keys())
        win_percentages = list(data.values())

        plt.bar(players, win_percentages)
        plt.xlabel('Players')
        plt.ylabel('Win Percentage (%)')
        plt.title('Player Performance in Monte Carlo Simulations')
        plt.show()
    
if __name__ == '__main__':
    
    verbose = False
    
    players = [
        Player('Player 1', DiscardBiggestStrategy(dhumbal_threshold=5, draw_graveyard_threshold=5), verbose=verbose), 
        Player('Player 2', DiscardBiggestStrategy(dhumbal_threshold=5, draw_graveyard_threshold=5), verbose=verbose), 
        Player('Player 3', MinimizeCardNumberStrategy(dhumbal_threshold=5, draw_graveyard_threshold=5, try_to_pool_threshold=2), verbose=verbose),
        ]

    mc = MonteCarlo(players, 20)
    mc.run_simulation()
    print([len(x) for x in mc.results])
    analysis = mc.analyze_results()
    print(analysis)
    # # mc.visualize_data(analysis)
    