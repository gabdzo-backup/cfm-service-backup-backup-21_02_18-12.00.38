"""Dish advisor."""

from typing import List, Optional, Tuple

from cfm_cms import recipe_parser as parser
from cfm_core.advice import Advice
from cfm_core.ingredient import Ingredient, RecipeIngredient
from cfm_core.pantry import Pantry
from cfm_core.recipe import Recipe


class DishAdvisor(object):
    """Dish advisor."""

    def __init__(self, recipes=None):
        """Constructor."""
        self.recipes = parser.load_recipes() if recipes is None else recipes

    def advise(self, pantry) -> List[Advice]:
        """Orchestrator to advise recipes.

        :param pantry: which pantry to use
        :return: advices: list of possible recipes
        """
        # given a pantry

        # find recipes for which pantry has at least one basic ingredient
        # (including alternatives)
        recipes = filter(lambda r: pantry.has_something_for(r), self.recipes)

        # for each of those recipes, find missing ingredients and their amounts
        advices: List[Advice] = [self._check_recipe(pantry, r) for r in recipes]

        # order by number of ingredients asc, not by the amount of ingredients
        return sorted(advices, key=lambda a: len(a.missing_ingredients))

    def _check_recipe(self, pantry: Pantry, recipe: Recipe) -> Advice:
        """Check if enough ingredients for recipe."""
        missing: List[Ingredient] = list()
        replacements: List[Tuple[Ingredient, Ingredient]] = list()

        for mi, replaced in map(
            lambda ri: self._check_ingredient(pantry, ri), recipe.ingredients
        ):
            if mi:
                missing.append(mi)
            if replaced:
                replacements.append((mi, replaced))

        return Advice(missing, recipe, replacements)

    @staticmethod
    def _check_ingredient(
        pantry: Pantry, ri: RecipeIngredient
    ) -> Tuple[Optional[Ingredient], Optional[Ingredient]]:
        """Check if pantry has enough ingredients."""
        if pantry.has(ri):
            # the pantry already has the ingredient, but maybe not enough
            if not pantry.has_enough(ri):
                needs = ri.amount - pantry.index[ri.id].amount
                return (
                    RecipeIngredient(ri.id, needs, ri.unit, ri.role, ri.alternative),
                    None,
                )
        elif ri.has_alternative() and pantry.has(ri.alternative):
            # the pantry has some of the alternative
            if not pantry.has_enough(ri.alternative):
                a = ri.alternative
                needs = ri.amount - pantry.index[a.id].amount
                return Ingredient(a.id, needs, a.unit), ri
        else:
            # need the whole amount of the basic or extra ingredient
            return ri, None

        return None, None
