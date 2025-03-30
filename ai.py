import random
from abc import ABC, abstractmethod

from moves import Move


class GameAIStrategy(ABC):
    @abstractmethod
    def select_move(self, moveset: list[Move], previous_rounds: list[tuple[Move, Move]]) -> Move:
        """
        Select a move for the AI based on the strategy.
        """
        pass


class RandomStrategy(GameAIStrategy):
    """
    Pure random strategy. (game-theory optimal for classic Rock, Paper, Scissors).
    Does not use the history of previous rounds.
    """
    def select_move(self, moveset: list[Move], previous_rounds: list[tuple[Move, Move]]) -> Move:
        return random.choice(moveset)


class ConstantStrategy(GameAIStrategy):
    """
    Always selects the first move. Useful for guaranteeing a user win during testing.

    Good old rock, nothing beats that: https://www.youtube.com/watch?v=b0SoKWLkmLU
    """
    def select_move(self, moveset: list[Move], previous_rounds: list[tuple[Move, Move]]) -> Move:
        return moveset[0]


class GameAI:
    def __init__(self, strategy: GameAIStrategy = None):
        self.strategy = strategy if strategy else RandomStrategy()
    
    def make_move(self, moveset: list[Move], previous_rounds: list[tuple[Move, Move]]) -> Move:
        """
        Get the AI move given a moveset and a history of previous rounds.
        
        Args:
            moveset: List of all possible moves
            previous_rounds: History of previous rounds (player_move, ai_move)
        
        Returns:
            The selected move for the AI
        """
        return self.strategy.select_move(moveset, previous_rounds)


def create_game_ai(strategy_name: str = "random") -> GameAI:
    match strategy_name:
        case "random":
            return GameAI(RandomStrategy())
        case "constant":
            return GameAI(ConstantStrategy())
        case _:
            raise ValueError(f"Unknown strategy: {strategy_name}")