from dataclasses import dataclass
from rules import RuleBook
from moves import Move, load_moveset


@dataclass
class GameState:
    rounds_to_win: int
    """Number of rounds a player needs to win."""
    rounds_won_player_1: int = 0
    """Rounds won by player 1 (humans)"""
    rounds_won_player_2: int = 0
    """Rounds won by player 2 (AI)"""
    player_has_won: int = -1
    """Indicates whether a certain player has won"""


@dataclass
class RoundResult:
    """Struct indicating the results of one round of RPS"""
    winner: int
    """Winning player 1 or 2, 0 indicates a draw."""
    feedback: str
    """Feedback string describing the result."""
    player_won_game: int = -1
    """Indicates a player won the game given the input and the current game state"""


class RulesEngine:
    """
    Core rules engine that processes moves and manages game state.
    Use this object to access the game state.

    Note: Reset game state or the Rules Engine object when a game has concluded.
    """

    def __init__(self, rule_book: RuleBook, best_of: int=3):
        assert best_of % 2 == 1, "best_of must be an odd number"
        
        self.game_state = GameState(
            rounds_to_win=(best_of // 2) + 1,
        )
        self.rule_book = rule_book
        self.moveset = load_moveset(self.rule_book.variant)

    def get_available_moves(self) -> list[Move]:
        """
        Returns all available moves
        """
        return self.moveset

    def input_moves(self, move_player_1: Move, move_player_2: Move) -> RoundResult:
        """
        Input a pair of moves updating the game state.
        The returned RoundResult object indicates whether a player won the game.
        """
        winner, verb = self.rule_book.who_wins(move_player_1, move_player_2)
        feedback = ""
        match winner:
            case 1:
                self.game_state.rounds_won_player_1 += 1
                feedback = f"{move_player_1.display_name} {verb} {move_player_2.display_name}"
            case 2:
                self.game_state.rounds_won_player_2 += 1
                feedback = f"{move_player_2.display_name} {verb} {move_player_1.display_name}"
            case 0:
                feedback = "This was a draw"
        
        player_won = -1
        if self.game_state.rounds_won_player_1 >= self.game_state.rounds_to_win:
            player_won = 1
            self.game_state.player_has_won = 1
        elif self.game_state.rounds_won_player_2 >= self.game_state.rounds_to_win:
            player_won = 2
            self.game_state.player_has_won = 2
            
        result = RoundResult(
            winner=winner, 
            feedback=feedback,
            player_won_game=player_won
        )
        
        return result
            
        





