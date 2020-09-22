"""Recipe model."""

from dataclasses import asdict, dataclass
from typing import List

from cfm_core import ingredient, step


@dataclass
class Recipe:
    """Model to represent recipe."""

    id: str
    title: str
    locale: str
    difficulty: str
    tools: List[str]
    ingredients: List[ingredient.RecipeIngredient]
    steps: List[step.Step]

    def asdict(self):
        """As dict."""
        return asdict(self)


def from_dict(id, title, locale, difficulty, tools, ingredients, steps):
    """From dict."""
    return Recipe(
        id=id,
        title=title,
        locale=locale,
        difficulty=difficulty,
        tools=tools,
        ingredients=[ingredient.RecipeIngredient.from_dict(i) for i in ingredients],
        steps=[step.from_dict(s) for s in steps],
    )
