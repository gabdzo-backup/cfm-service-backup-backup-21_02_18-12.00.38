"""Docstring."""

import logging
from typing import List

from cfm_core.advice import Advice
from cfm_disadvisor.dish_advisor import DishAdvisor
from storage.memory_storage import InMemoryCfmStorage


class ServerImpl(object):
    """Docstring."""

    def __init__(self, storage_type):
        """Docstring."""
        self.dishadvisor = DishAdvisor()

        if storage_type == "memory":
            self.storage = InMemoryCfmStorage()

    def advise_pantry(self, pantry_id: str) -> List[Advice]:
        """Docstring."""
        logging.info("Advising recipes for pantryId:{}".format(pantry_id))
        pantry = self.storage.get_pantry(pantry_id)
        return self.dishadvisor.advise(pantry)
