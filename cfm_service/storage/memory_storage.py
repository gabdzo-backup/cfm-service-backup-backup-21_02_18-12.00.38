"""Docstring."""

from typing import Dict

from cfm_core.ingredient import Ingredient
from cfm_core.pantry import Pantry
from cfm_service.storage import CfmStorage


class InMemoryCfmStorage(CfmStorage):
    """Docstring."""

    def __init__(self):
        """Docstring."""
        self.pantries: Dict[str, Pantry] = {
            "-1": Pantry([Ingredient("egg", 1, "piece")])
        }
        self.next_id = 0

    def store_pantry(self, user_id: str, pantry_id: str, pantry: Pantry) -> str:
        """Docstring."""
        self.pantries[pantry_id] = pantry
        return pantry_id

    def get_pantry(self, pantry_id: str) -> Pantry:
        """Docstring."""
        return self.pantries.get(pantry_id)
