import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import math
import numpy as np

from trueskill import setup, Rating, rate, TrueSkill

class TrueskillDhumbal:
    def __init__(self, mc, players, mu=1000, sigma=300, beta=4000, tau=0.1, draw_probability=0):
        
        # Initialize TrueSkill environment
        setup(mu=mu, sigma=sigma, beta=beta, tau=tau, draw_probability=draw_probability)
        
        # Initialize player stats
        self.mc = mc
        self.players = players
        self.player_stats = mc.player_stats
        self.ranking_progression_windows = []
        self.reset_ratings()
        
    def reset_ratings(self):
        for player in self.players:
            self.player_stats[player.name]["trueskill_rating"] = Rating()
        self.ranking_progression = {player.name: [] for player in self.players}
        
        
    def run_simulation(self, window, batches, function):
        
        assert(batches * window <= self.mc.num_simulations)
        
        self.ranking_progression_windows = []
        
        for i in range(batches):
            print(f'Current batch: {i} / {batches}', end='\r')
            window_run = function(window, start_index=i*window)
            self.ranking_progression_windows.append(window_run)
    
    def ratings_game_outcome(self, number_of_games, start_index=0):
        
        self.reset_ratings()
        
        for i in range(number_of_games):
            # Create game results based on player positions
            game_results = [(player.name, self.player_stats[player.name]['positions'][start_index+i]) for player in self.players]
            sorted_results = sorted(game_results, key=lambda x: x[1])

            # Extract ratings for the rate function
            rated_players = [(self.player_stats[name]['trueskill_rating'],) for name, _ in sorted_results]

            # Update ratings
            new_ratings = rate(rated_players, ranks=[rank for _, rank in sorted_results])

            # Unpack new ratings and update player_stats
            for ((name, _), (new_rating,)) in zip(sorted_results, new_ratings):
                self.player_stats[name]['trueskill_rating'] = new_rating
                self.ranking_progression[name].append((new_rating.mu, new_rating.sigma))
                
        return self.ranking_progression
                
    def ratings_round_outcome(self, number_of_games, start_index=0):
        
        self.reset_ratings()
        
        for i, game in enumerate(self.mc.results[start_index:start_index + number_of_games]):
            setup(mu=1000, sigma=50, beta=4000, tau=0.001, draw_probability=0)
            for round in game:
                # Create game results based on player scores in this round
                game_results = [(player, round[player][0]) for player in round]
                sorted_results = sorted(game_results, key=lambda x: x[1])  # Sort based on scores, lowest is better

                # Extract ratings for the rate function
                rated_players = [(self.player_stats[player.name]['trueskill_rating'],) for player, _ in sorted_results]

                # Update ratings
                new_ratings = rate(rated_players, ranks=[rank for _, rank in sorted_results])

                # Unpack new ratings and update player_stats and ranking_progression
                for ((player, _), (new_rating,)) in zip(sorted_results, new_ratings):
                    player_name = player.name
                    self.player_stats[player_name]['trueskill_rating'] = new_rating
                    self.ranking_progression[player_name].append((new_rating.mu, new_rating.sigma))
                    
        return self.ranking_progression
    
    def plot_ratings_windows(self):
        # Initialize dictionary to store means for each player at each step
        player_means = {}

        for sim in self.ranking_progression_windows:
            for player, values in sim.items():
                if player not in player_means:
                    player_means[player] = []
                # Append only the means, ignoring the irrelevant number
                player_means[player].append([mean for mean, _ in values])

        # Find the minimum number of steps for each player
        min_steps = {player: min(len(steps) for steps in player_means[player]) for player in player_means}

        # Truncate the data to the minimum number of steps for each player
        for player in player_means:
            player_means[player] = [steps[:min_steps[player]] for steps in player_means[player]]

        # Transpose the list of lists to get step-wise data
        for player in player_means:
            player_means[player] = list(map(list, zip(*player_means[player])))

        # Calculate mean of means and std of means for each step for each player
        stats = {player: {'mean_of_means': [], 'std_of_means': []} for player in player_means}

        for player, steps in player_means.items():
            for step_means in steps:
                stats[player]['mean_of_means'].append(np.mean(step_means))
                stats[player]['std_of_means'].append(np.std(step_means))

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))

        for player in player_means:
            means = stats[player]['mean_of_means']
            std_dev = stats[player]['std_of_means']
            steps = np.arange(len(means))

            # Plot mean
            ax.plot(steps, means, label=f"{player} Mean of Means")

            # Plot std deviation as a band
            ax.fill_between(steps, np.array(means) - np.array(std_dev), 
                            np.array(means) + np.array(std_dev), alpha=0.2)

        ax.set_title("Evolution of Mean of Means with Standard Deviation")
        ax.set_xlabel("Step Number")
        ax.set_ylabel("Mean of Means")
        ax.legend()

        plt.tight_layout()
        plt.show()
    
    def plot_ratings(self):

        # Assuming ranking_progression is already filled with TrueSkill data
        # ranking_progression = ...

        # Preparing DataFrame for Seaborn
        
        data_for_plot = []
        for name, ratings in self.ranking_progression.items():
            for iteration, (mu, sigma) in enumerate(ratings):
                data_for_plot.append({'Player': name, 'Iteration': iteration, 'Mu': mu, 'Sigma': sigma})
                
        df = pd.DataFrame(data_for_plot)

        # Set up the plot with two subplots
        fig, axes = plt.subplots(1, 2, figsize=(18, 6))
        sns.set(style="whitegrid")

        # Line plot for the mean (mu) on the left subplot
        sns.lineplot(ax=axes[0], x='Iteration', y='Mu', hue='Player', data=df, legend='full')
        for name in self.ranking_progression.keys():
            player_df = df[df['Player'] == name]
            axes[0].fill_between(player_df['Iteration'], player_df['Mu'] - player_df['Sigma'], player_df['Mu'] + player_df['Sigma'], alpha=0.2)
        axes[0].set_title('TrueSkill Rating Progression for Each Player')
        axes[0].set_xlabel('Iteration')
        axes[0].set_ylabel('TrueSkill Mu (with Sigma Confidence Interval)')

        # Normal distribution plot for the mu values on the right subplot
        for name in self.ranking_progression.keys():
            player_df = df[df['Player'] == name]
            sns.kdeplot(ax=axes[1], data=player_df['Mu'], label=name)
        axes[1].set_title('Normal Distribution of Mu Values for Each Player')
        axes[1].set_xlabel('Mu Value')
        axes[1].set_ylabel('Density')
        axes[1].legend(title='Player')

        plt.tight_layout()
        plt.show()

    
    def get_player_rating(self, player_name):
        return self.player_stats[player_name]["trueskill_rating"]
    
    def get_all_player_ratings(self):
        # Checking the updated rating
        for player in self.players:
            print(player.name, self.player_stats[player.name]["trueskill_rating"])
            
            
    def win_probability(team1, team2, beta=4000):
        delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
        sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
        size = len(team1) + len(team2)
        denom = math.sqrt(size * (beta * beta) + sum_sigma)
        return TrueSkill().cdf(delta_mu / denom)



# Example usage:
# Assuming players is a list of player objects with 'name' and 'positions' attributes
# trueskill_dhumbal = TrueskillDhumbal(players)
# trueskill_dhumbal.update_ratings(ZOOM_NUMBER_GAMES)
# print(trueskill_dhumbal.get_player_rating("PlayerName"))
