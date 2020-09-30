"""Pantry mode."""

from dataclasses import asdict, dataclass
from typing import Dict, List

from cfm_core import ingredient, recipe


@dataclass
class Pantry:
    """Model to represent pantry."""

    # needed at creation time
    ingredients: List[ingredient.Ingredient]

    # populated during post_init
    index: Dict[str, ingredient.Ingredient] = None

    def __post_init__(self):
        """Magic post init."""
        self.index = {i.id: i for i in self.ingredients}

    def __str__(self) -> str:
        """Docstring."""
        return ",".join([str(i) for i in self.ingredients])

    def asdict(self):
        """As dict."""
        return asdict(self)

    def has(self, i: ingredient.Ingredient) -> bool:
        """Check if ingredient is in pantry.

        :param i:
        :return: true if the ingredient is in pantry
        """
        if isinstance(i, ingredient.Ingredient):
            i = i.id
        return i in self.index.keys()

    def has_enough(self, i: ingredient.Ingredient) -> bool:
        """Check if enough quantity for recipe."""
        return self.has(i) and self.index[i.id].amount >= i.amount

    def has_something_for(self, r: recipe.Recipe) -> bool:
        """Has something for."""
        return any(map(lambda i: self.has(i) or self.has(i.alternative), r.ingredients))

    @staticmethod
    def from_str(string: str):
        """Reconstruct a pantry from its string representation.

        :param string: an output of str(pantry)
        :return: a pantry object
        """
        it = iter(string.split(","))
        tuples = [(x, next(it), next(it)) for x in it]
        ingredients = [
            ingredient.Ingredient(id=name, amount=amount, unit=unit)
            for (name, amount, unit) in tuples
        ]
        return Pantry(ingredients)
