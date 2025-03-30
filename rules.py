import json
import os

from moves import Move


def load_rules() -> dict:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data/rules.json')

    with open(json_path, 'r') as fp:
        rules = json.load(fp)

    return rules


class Rules:
    """
    Loads rules in a data-driven way from the rules json config file,
    supporting multiple different rules versions.
    """

    def __init__(self):
        self._rules_per_variant = load_rules()['rule_variant']
        self._variants = list(self._rules_per_variant.keys())

    @property
    def variants(self) -> list[str]: 
        return self._variants
    
    def get_rule_book_for_variant(self, variant='classic'):
        return RuleBook(self._rules_per_variant[variant], variant)


class RuleBook:
    """
    Rulebook for a specific game variant.

    Determines winner and loser for a given tuple of moves.
    """

    def __init__(self, rules_dict: dict, variant: str):
        self._rules = rules_dict
        self.variant = variant

    def who_wins(self, move1: Move, move2: Move) -> tuple[int, str]:
        if move1.name == move2.name:
            return 0, "draw"
        if move2.name in self._rules[move1.name]['beats']:
            return 1, self._rules[move1.name]['beats'][move2.name]['verb']
        elif move1.name in self._rules[move2.name]['beats']:
            return 2, self._rules[move2.name]['beats'][move1.name]['verb']
        else:
            raise RuntimeError("Incomplete ruleset. This should not happen")
