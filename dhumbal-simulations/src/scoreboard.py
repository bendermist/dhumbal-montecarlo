from cards import Result


class Scoreboard:
    def __init__(self, players):
        self.scores = {player: 0 for player in players}  # Stores cumulative scores for each player
        self.round_log = []  # Stores the results of each round

    def record_round(self, game):
        # Update cumulative scores after each round
        round_log = {}
        
        dhumbal_caller = next((player for player in game.players if player.called_dhumbal), None)
        
        if not dhumbal_caller:
            return ValueError("No player called Dhumbal")
        
        dhumbal_caller_score = dhumbal_caller.calculate_score()
        lowest_score = min(player.calculate_score() for player in game.players)

        for player in game.players:
            score = player.calculate_score()
            if player == dhumbal_caller:
                if dhumbal_caller_score < lowest_score:
                    self.scores[player] += score
                    round_log[player] = (score, Result.DHUMBAL)
                else:
                    self.scores[player] += 20
                    round_log[player] = (score, Result.GOT_DESTROYED)
            else:
                self.scores[player] += score
                if score <= dhumbal_caller_score:
                    round_log[player] = (score, Result.DESTROYED)
                else:
                    round_log[player] = (score, Result.NORMAL)
        
        self.round_log.append(round_log)
                


    def get_scores(self):
        # Return the current scores
        return self.scores

    def get_eliminated_players(self):
        # Return a list of players who have 108 points or more
        return [player for player, score in self.scores.items() if score >= 108]
    
    def get_last_player(self):
        # Return the index of the last player in the previous round
        if len(self.round_log) == 0:
            return 0
        player_scores = {player: score_info[0] for player, score_info in self.round_log[-1].items()}
        worst_scorer = max(player_scores, key=player_scores.get)
        return worst_scorer