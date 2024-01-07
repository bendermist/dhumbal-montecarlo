from collections import defaultdict
import matplotlib.pyplot as plt

from cards import Deck
from game import Game
from player import Player, DiscardBiggestStrategy, MinimizeCardNumberStrategy

class MonteCarlo:
    def __init__(self, players, num_simulations, verbose=False):
        self.num_simulations = num_simulations
        self.players = players
        self.verbose = verbose
        self.game = Game(self.players, self.verbose) # Game object used to run simulations
        
        
    def run_simulation(self):
        results = []
        for i in range(self.num_simulations):
            self.game = Game(self.players, self.verbose)  # Reset the game
            self.game.start_game()
            results.append(self.game.scoreboard.round_log)
            print(f'Current iteration: {i} / {self.num_simulations}', end='\r')
        self.results = results

    def analyze_results(self):
        player_positions = defaultdict(lambda: defaultdict(int))
        completed_games = [result for result in self.results if len(result) > 0]
        print(len(self.results) - len(completed_games), "out of", len(self.results), "games ended in a draw")

        for simulation in completed_games:
            last_round = simulation[-1]
            # Sort players based on score_total, score_at_round, and Result.value
            sorted_players = sorted(
                last_round.items(), 
                key=lambda x: (x[1][1], x[1][0], x[1][2].value)
            )
            # Count positions for each player
            for position, (player, _) in enumerate(sorted_players, start=1):
                player_positions[player][position] += 1

        # Calculate position probabilities
        position_probabilities = {player.name: {position: count / len(completed_games) * 100 * len(self.players) 
                                                for position, count in positions.items()}
                                for player, positions in player_positions.items()}

        return position_probabilities

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
        Player('Player 4', MinimizeCardNumberStrategy(dhumbal_threshold=5, draw_graveyard_threshold=5, try_to_pool_threshold=2), verbose=verbose),
        Player('Player 5', MinimizeCardNumberStrategy(dhumbal_threshold=5, draw_graveyard_threshold=5, try_to_pool_threshold=2), verbose=verbose),
        ]

    mc = MonteCarlo(players, 200, verbose=verbose)
    mc.run_simulation()
    print([len(x) for x in mc.results])
    analysis = mc.analyze_results()
    print(analysis)
    # # mc.visualize_data(analysis)
    