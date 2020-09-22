"""Recipe parser."""

import logging
import os
from pathlib import Path
from typing import Iterator

from cfm_core import recipe
import yaml


# default path is relative from this script, two times up and then into cms/en-us folder
DEFAULT_CMS_PATH = (
    Path("../..") / Path(os.path.realpath(__file__)).parent / Path("cms/en-us")
)


def _traverse_folder(root_path):
    """Traverse recipe folder.

    :param root_path: where to look for files
    :return: every yaml file found under root_path, recursively
    """
    p = Path(root_path)
    logging.debug("Looking for recipes from root folder {}".format(p.absolute()))
    for filename in p.rglob("*yaml"):
        yield filename


def parse_yaml_file(path_to_file) -> recipe.Recipe:
    """Parse yaml recipe file."""
    with open(path_to_file, "r") as stream:
        try:
            return recipe.from_dict(**yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)


def load_recipes(cms_path=DEFAULT_CMS_PATH) -> Iterator[recipe.Recipe]:
    """Load recipes."""
    all_files = _traverse_folder(cms_path)
    for file in all_files:
        yield parse_yaml_file(file)
