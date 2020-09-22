"""Test recipe parser."""
import unittest

from cfm_cms.recipe_parser import load_recipes


class RecipeParserTest(unittest.TestCase):
    """Test recipe parser."""

    def __init__(self, *args, **kwargs):
        """__init__."""
        super().__init__(*args, **kwargs)

    def test_parse_recipes(self):
        """Test parse recipes."""
        recipes = load_recipes()
        self.assertEqual(2, len(list(recipes)))

    def test_alternative_parses_correctly(self):
        """Test alternative recipes correctly."""
        recipes = load_recipes()
        recipe = [r for r in recipes if r.id == "pumpkin-soup"][0]
        cream = [i for i in recipe.ingredients if i.id == "cream"][0]
        alt = cream.alternative
        self.assertEqual("coconut cream", alt.id)
