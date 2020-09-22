"""Ingredient model."""

from dataclasses import asdict, dataclass
from enum import Enum


@dataclass
class Ingredient:
    """Model to represent ingredient."""

    id: str
    amount: int
    unit: str

    def __eq__(self, other):
        """Magic eq method."""
        return self.id == other.name

    def asdict(self):
        """Return as dictionary."""
        return asdict(self)


class IngredientRole(Enum):
    """Ingredient role."""

    BASIC = 1
    EXTRA = 2
    ALTERNATIVE = 3


@dataclass
class RecipeIngredient(Ingredient):
    """Relation model from recipe to ingredient."""

    role: IngredientRole
    alternative: Ingredient = None

    def has_alternative(self) -> bool:
        """Check if ingredient has alternative."""
        return self.alternative is not None

    @staticmethod
    def from_dict(ingredient_dict):
        """Get ingredients from dict."""
        assert len(ingredient_dict) == 1
        for k, v in ingredient_dict.items():
            return RecipeIngredient._from_dict(IngredientRole[k.upper()], **v)

    @staticmethod
    def _from_dict(role, id, amount, unit, alternative=None):
        """From dict handle."""
        return RecipeIngredient(
            id=id,
            amount=amount,
            unit=unit,
            role=role,
            alternative=RecipeIngredient._from_dict(
                IngredientRole.ALTERNATIVE, **alternative
            )
            if alternative is not None
            else None,
        )
