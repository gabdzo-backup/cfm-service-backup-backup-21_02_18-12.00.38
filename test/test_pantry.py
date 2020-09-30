"""Test recipe parser."""
import unittest

from cfm_core import ingredient, pantry


class PantryTest(unittest.TestCase):
    """Testing pantry class."""

    def __init__(self, *args, **kwargs):
        """__init__."""
        super().__init__(*args, **kwargs)

    def test_parse_to_string(self):
        """Test converting pantry to string."""
        i = ingredient.Ingredient(id="egg", amount=1, unit="pc")
        p = pantry.Pantry([i])
        self.assertEqual("egg,1,pc", str(p))

    def test_parse_from_string(self):
        """Test getting pantries from strings."""
        s = "egg,1,pc"
        p = pantry.Pantry.from_str(s)
        expected = pantry.Pantry([ingredient.Ingredient("egg", 1, "pc")])
        self.assertEqual(expected, p)

        s = "egg,1,pc,flour,0.5,kg"
        p = pantry.Pantry.from_str(s)
        expected = pantry.Pantry(
            [
                ingredient.Ingredient("egg", 1, "pc"),
                ingredient.Ingredient("flour", 0.5, "kg"),
            ]
        )
        self.assertEqual(expected, p)
