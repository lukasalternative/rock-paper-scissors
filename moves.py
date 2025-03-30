import json
import os
from pydantic import BaseModel


class Move(BaseModel):
    """
    A move in the game Rock, Papers, Scissors (or its variants).
    Made by human player or AI.
    """
    name: str
    """Internal name"""
    display_name: str
    """The displayed name of the move"""
    variants: list[str]
    """List of game variants this move is valid for"""


def load_moveset(variant:str ='classic'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data/moves.json')

    with open(json_path, 'r') as fp:
        move_dicts = json.load(fp)['moves']
    
    move_dicts = [m for m in move_dicts if variant in m['variants']]
    moves = [Move(**m) for m in move_dicts]

    return moves
