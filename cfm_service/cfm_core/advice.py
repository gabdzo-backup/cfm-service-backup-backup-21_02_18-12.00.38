"""Advice model."""
from dataclasses import asdict, dataclass
from typing import List, Tuple

from cfm_core.ingredient import Ingredient
from cfm_core.recipe import Recipe


@dataclass
class Advice:
    """Model to represent advice."""

    missing_ingredients: List[Ingredient]
    recipe: Recipe
    replacements: List[Tuple[Ingredient, Ingredient]] = None

    def asdict(self):
        """Return as dictionary."""
        return asdict(self)
