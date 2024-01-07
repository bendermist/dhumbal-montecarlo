from collections import Counter, OrderedDict
import numpy as np
import matplotlib.pyplot as plt

from game import Game
from player import Player, DiscardBiggestStrategy, MinimizeCardNumberStrategy

class MonteCarlo:
    def __init__(self, players, num_simulations, verbose=False):
        self.num_simulations = num_simulations
        self.players = players
        self.verbose = verbose
        self.game = Game(self.players, self.verbose) # Game object used to run simulations
        self.player_stats = {} # intermediate data structure to store data for each player
        self.player_statistics = {} #summary of performance across all games
        
        
    def run_simulation(self):
        results = []
        for i in range(self.num_simulations):
            self.game = Game(self.players, self.verbose)  # Reset the game
            self.game.start_game()
            results.append(self.game.scoreboard.round_log)
            print(f'Current iteration: {i} / {self.num_simulations}', end='\r')
        self.results = results

    def analyze_results(self):

        mc_results = self.results
        for game_list in mc_results:
            # Temporary structure to store data for position calculation
            temp_positions = {}
            for game in game_list:
                for player, player_data in game.items():
                    player_name = player.name  # Assuming each player key has a 'name' attribute
                    if player_name not in self.player_stats:
                        self.player_stats[player_name] = {'scores': [], 'outcomes': [], 'rounds_played': 0, 'final_points': [], 'last_round_points': []}
                    self.player_stats[player_name]['scores'].append(player_data[0])
                    self.player_stats[player_name]['outcomes'].append(player_data[2])
                    # Update rounds played, final points, and last round points
                    self.player_stats[player_name]['rounds_played'] += 1
                    self.player_stats[player_name]['final_points'].append(player_data[1])
                    self.player_stats[player_name]['last_round_points'].append(player_data[0])
                    # Store in temp structure for position calculation
                    temp_positions[player_name] = self.player_stats[player_name]

            # Calculate positions
            sorted_positions = sorted(temp_positions.items(), key=lambda x: (x[1]['rounds_played'], -x[1]['final_points'][-1], x[1]['last_round_points'][-1]), reverse=True)
            for position, (player_name, _) in enumerate(sorted_positions, start=1):
                if 'positions' not in self.player_stats[player_name]:
                    self.player_stats[player_name]['positions'] = []
                self.player_stats[player_name]['positions'].append(position)
                
                self.player_stats[player_name]['rounds_played'] = 0
                self.player_stats[player_name]['final_points'].clear()
                self.player_stats[player_name]['last_round_points'].clear()


        # Compute statistics for each player
        for player_name, data in self.player_stats.items():
            mean_score = np.mean(data['scores'])
            std_deviation = np.std(data['scores'])
            variance = np.var(data['scores'])
            outcome_frequency = Counter(data['outcomes'])
            total_games = len(data['scores'])
            outcome_percentages = {outcome: (count / total_games) * 100 for outcome, count in outcome_frequency.items()}
            self.player_statistics[player_name] = {'mean_score': mean_score, 'std_deviation': std_deviation, 
                                    'variance': variance, 'outcome_percentages': outcome_percentages}
            
    def player_position_probabilities(self):
        position_probabilities = {}

        # Calculate probabilities
        for player_name, stats in self.player_stats.items():
            total_games = len(stats['positions'])
            position_counts = Counter(stats['positions'])
            sorted_positions = OrderedDict(sorted(position_counts.items()))
            position_probabilities[player_name] = {position: count / total_games for position, count in sorted_positions.items()}

        # Sort by player names
        sorted_position_probabilities = OrderedDict(sorted(position_probabilities.items()))
        return sorted_position_probabilities


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
    