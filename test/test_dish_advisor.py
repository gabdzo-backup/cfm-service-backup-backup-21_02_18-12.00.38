"""Unit tests for dish_advisor package."""
import unittest


from cfm_core import ingredient
from cfm_core.pantry import Pantry
from cfm_disadvisor.dish_advisor import DishAdvisor


class DishAdvisorTest(unittest.TestCase):
    """Unit tests for dish_advisor package."""

    def __init__(self, *args, **kwargs):
        """__init__."""
        super().__init__(*args, **kwargs)

    def test_empty_pantry(self):
        """Tests empty pantry."""
        pantry = Pantry([])
        advices = DishAdvisor().advise(pantry)
        # for an empty pantry, we don't recommend anything
        self.assertEqual(0, len(advices))

    def test_advice_when_having_one_egg(self):
        """Check if advice is given when having one egg."""
        pantry = Pantry([ingredient.Ingredient("egg", 1, "piece")])
        adviser = DishAdvisor()
        advices = adviser.advise(pantry)

        # we expect one advice
        self.assertEqual(1, len(advices))
        advice = advices[0]

        # we expect all these ingredients to show up in the advice.
        # the mushroom is an extra ingredient, and it shows up anyway!
        expected_ingredients = {"egg", "onion", "garlic", "mushroom"}
        advised_ingredients = set(map(lambda i: i.id, advice.missing_ingredients))
        self.assertEqual(expected_ingredients, advised_ingredients)

        for mi in advice.missing_ingredients:
            # we also expect one of the missing ingredients to be 2 eggs
            if mi.id == "egg":
                self.assertEqual(2, mi.amount)

        # make sure the advice is reproducible
        advices = adviser.advise(pantry)
        self.assertEqual(1, len(advices))

    def test_pair_replacements(self):
        """Test pair replacements."""
        # define recipe ingredients so that carrot replaces a plasternaka
        carrot = ingredient.Ingredient("carrot", 2, "piece")
        recipe_plasternaka = ingredient.RecipeIngredient(
            "plasternaka",
            2,
            "piece",
            ingredient.IngredientRole.ALTERNATIVE,
            alternative=carrot,
        )

        # put just 1 carrot into pantry
        pantry = Pantry([ingredient.Ingredient("carrot", 1, "piece")])

        # check that carrot indeed replaces plasternaka
        missing, replaced = DishAdvisor._check_ingredient(pantry, recipe_plasternaka)

        self.assertTrue(replaced is not None)
        self.assertTrue(missing is not None)
        self.assertEqual("plasternaka", replaced.id)
        self.assertEqual("carrot", missing.id)
        self.assertEqual(1, missing.amount)

    def test_advice_with_alternative(self):
        """Test advice with alternative."""
        pantry = Pantry([ingredient.Ingredient("coconut cream", 400, "ml")])
        advices = DishAdvisor().advise(pantry)

        # we expect one advice
        self.assertEqual(1, len(advices))
        advice = advices[0]

        # it's the pumpkin soup, and it needs 4 ingredients
        self.assertEqual("pumpkin-soup", advice.recipe.id)
        self.assertEqual(4, len(advice.missing_ingredients))
        # and there's no cream nor coconut cream
        missing = {i.id for i in advice.missing_ingredients}
        self.assertFalse("cream" in missing)
        self.assertFalse("coconut cream" in missing)
