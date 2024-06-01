from collections import OrderedDict
import logging
import os
from os import walk
import random

logger = logging.getLogger(__name__)


def load_names(path):
    logger.debug(path)
    name_replacements = OrderedDict()
    file_names = next(walk(path), (None, None, []))[2]  # [] if no file
    file_names.sort()

    for filename in file_names:
        if filename.startswith("."):
            continue

        name_type = os.path.splitext(filename)[0]

        with open(os.path.join(path, filename)) as f:
            name_replacements[name_type] = f.read().splitlines()
            random.shuffle(name_replacements[name_type])
        f.close()

    return name_replacements


def load_name_replacements():
    resource_directory = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "resources"
    )
    names_directory = os.path.join(resource_directory, "names")
    replacements_directory = os.path.join(names_directory, "replace")

    return load_names(replacements_directory)


def load_name_recognizers():
    resource_directory = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "resources"
    )
    names_directory = os.path.join(resource_directory, "names")
    recognizers_directory = os.path.join(names_directory, "recognize")

    return load_names(recognizers_directory)
