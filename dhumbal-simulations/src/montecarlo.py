from game import Game
from player import Player


class MonteCarlo:
    def __init__(self, num_simulations):
        self.num_simulations = num_simulations

    def run_simulation(self):
        results = []
        for _ in range(self.num_simulations):
            game = Game()
            while not game.is_over():
                game.play_round()
            results.append(game.winner())
        return results

    def analyze_results(self, results):
        # TODO: Implement analysis of results
        pass

    def visualize_data(self, data):
        # TODO: Implement data visualization
        pass
    
if __name__ == '__main__':
    players = [Player('Player 1'), Player('Player 2'), Player('Player 3')]
    game = Game(players)
    game.start_game()