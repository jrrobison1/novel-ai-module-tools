from collections import OrderedDict
from pathlib import Path
import random

from novel_ai_module_tools.logger_config import get_logger


logger = get_logger(__file__)


def load_names(path):
    """
    Load names from files in the specified directory.

    Args:
        path (Path): The directory path containing name files.

    Returns:
        OrderedDict: A dictionary where keys are name types (based on filenames)
                     and values are shuffled lists of names.
    """
    logger.info(f"Loading names from path: [{path}]")
    name_replacements = OrderedDict()
    file_names = sorted([f.name for f in path.iterdir() if f.is_file()])

    for filename in file_names:
        logger.info(f"Loading names from file: [{filename}]")
        if filename.startswith("."):
            continue

        name_type = Path(filename).stem

        with open(path / filename) as f:
            name_replacements[name_type] = f.read().splitlines()
            random.shuffle(name_replacements[name_type])

    return name_replacements


def load_name_replacements():
    """
    Load name replacements from the 'replace' directory.

    Returns:
        OrderedDict: A dictionary of name replacements.
    """
    resource_directory = Path(__file__).parent / "resources"
    names_directory = resource_directory / "names"
    replacements_directory = names_directory / "replace"

    return load_names(replacements_directory)


def load_name_recognizers():
    """
    Load name recognizers from the 'recognize' directory.

    Returns:
        OrderedDict: A dictionary of name recognizers.
    """
    resource_directory = Path(__file__).parent / "resources"
    names_directory = resource_directory / "names"
    recognizers_directory = names_directory / "recognize"

    return load_names(recognizers_directory)
