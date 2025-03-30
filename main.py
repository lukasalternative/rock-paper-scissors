import os
import time

from ai import create_game_ai
from config import GameVariant, load_config
from moves import Move
from rules import Rules
from rules_engine import RulesEngine, GameState, RoundResult


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_odd_number(prompt: str, default: int = 3) -> int:
    """Get an odd number from user input."""
    while True:
        try:
            value = input(f"{prompt} [{default}]: ").strip()
            if not value:
                return default
            
            number = int(value)
            if number % 2 == 0:
                print("Please enter an odd number.")
                continue
            
            if number <= 0:
                print("Please enter a positive number.")
                continue
                
            return number
        except ValueError:
            print("Please enter a valid number.")


def select_game_variant(variants: list[GameVariant]) -> str:
    print("\nSelect game variant:")
    print("=" * 20)
    
    for i, variant in enumerate(variants, 1):
        print(f"{i}. {variant.display_name}")
    
    while True:
        try:
            choice = input("\nYour choice (number): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(variants):
                return variants[choice_idx].name
            else:
                print(f"Please enter a number between 1 and {len(variants)}.")
        except ValueError:
            print("Please enter a valid number.")


def display_moves(available_moves: list[Move]) -> int:
    """Display available moves and get player choice."""
    print("\nChoose your move:")
    print("=" * 20)
    
    for i, move in enumerate(available_moves, 1):
        print(f"{i}. {move.display_name}")
    
    while True:
        try:
            choice = input("\nYour choice (number): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(available_moves):
                return choice_idx
            else:
                print(f"Please enter a number between 1 and {len(available_moves)}.")
        except ValueError:
            print("Please enter a valid number.")


def display_game_state(game_state: GameState, round_number: int):
    print("\n" + "=" * 40)
    print(f"Round {round_number}")
    print(f"Score: Player {game_state.rounds_won_player_1} - {game_state.rounds_won_player_2} AI")
    print(f"First to {game_state.rounds_to_win} wins!")
    print("=" * 40)


def display_round_result(round_result: RoundResult, player_move: Move, ai_move: Move):
    print("\n" + "-" * 40)
    
    if round_result.winner == 0:
        print("It's a tie!")
    elif round_result.winner == 1:
        print("You win this round!")
    else:
        print("AI wins this round!")
    
    print(f"You chose: {player_move.display_name}")
    print(f"AI chose: {ai_move.display_name}")
    
    if round_result.feedback:
        print(f"Result: {round_result.feedback}")
    
    print("-" * 40)


def display_game_result(game_state: GameState):
    """Display the final game result."""
    print("\n" + "*" * 50)
    
    if game_state.player_has_won == 1:
        print("🎉 Congratulations! You won the game! 🎉")
    else:
        print("Better luck next time! The AI won the game.")
    
    print(f"Final Score: Player {game_state.rounds_won_player_1} - {game_state.rounds_won_player_2} AI")
    print("*" * 50)


def main():
    """Main game loop."""
    clear_screen()
    print("Welcome to Rock Paper Scissors!")
    print("-----------------------------------")
    
    conf = load_config()

    rules = Rules()
    
    variant = select_game_variant(conf.variants)
    
    rule_book = rules.get_rule_book_for_variant(variant)
    
    best_of = get_odd_number("Choose 'best of' games (must be odd number)", 3)
    
    ai = create_game_ai(conf.ai_strategy)
    
    rules_engine = RulesEngine(rule_book, best_of)
    
    playing = True
    while playing:
        round_number = 1
        previous_rounds = []
        
        # Round loop
        while True:
            clear_screen()
            display_game_state(rules_engine.game_state, round_number)
            
            available_moves = rules_engine.get_available_moves()
            
            player_choice_idx = display_moves(available_moves)
            player_move = available_moves[player_choice_idx]
            
            print("\nAI is making a move...")
            time.sleep(0.5)
            
            ai_move = ai.make_move(available_moves, previous_rounds)
            round_result = rules_engine.input_moves(player_move, ai_move)
            previous_rounds.append((player_move, ai_move))
            
            display_round_result(round_result, player_move, ai_move)
            
            if round_result.player_won_game >= 0:
                display_game_result(rules_engine.game_state)
                
                play_again = input("\nWould you like to play again? (y/n): ").strip().lower()
                if play_again != 'y':
                    print("\nThanks for playing!")
                    playing = False
                    break
                    
                # Reset the game
                rule_book = rules.get_rule_book_for_variant(variant)
                rules_engine = RulesEngine(rule_book, best_of)
                break
            else:
                round_number += 1
                input("\nPress Enter to continue to the next round...")


if __name__ == "__main__":
    main()