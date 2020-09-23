"""Docstring."""

from cfm_core.pantry import Pantry


class CfmStorage(object):
    """Docstring."""

    def store_pantry(self, user_id: str, pantry_id: str, pantry: Pantry) -> str:
        """Docstring."""
        raise NotImplementedError

    def get_pantry(self, pantry_id: str) -> Pantry:
        """Docstring."""
        raise NotImplementedError
