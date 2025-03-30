import json
import os
from pydantic import BaseModel


class GameVariant(BaseModel):
    name: str
    """The internal name"""
    display_name: str
    "The name of the game variant displayed to the user"


class GameConfig(BaseModel):
    variants: list[GameVariant]
    """The game variants available"""
    ai_strategy: str
    """The strategy employed by the AI"""


def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data/gameconf.json')

    with open(json_path, 'r') as fp:
        data = json.load(fp)
        return GameConfig(**data)