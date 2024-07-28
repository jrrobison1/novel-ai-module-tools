import logging
import sys
from typing import Dict, Union

from novel_ai_module_tools.logger_config import get_logger

STAR_SEPARATOR = "***"
FIRST_HALF = "first_half"
SECOND_HALF = "second_half"
NO_STARS = "no_stars"
FULL_TEXT = "full_text"


logger = get_logger(__file__)


def get_star_index(input_text: str) -> int:
    """
    Find the index of the first occurrence of '***' in the second half of the input text.

    Args:
        input_text (str): The input text to search.

    Returns:
        int: The index of '***' in the second half of the text, or -1 if not found.
    """
    logger.info(f"String length: {len(input_text)}")
    midway_index = int(len(input_text) / 2)
    logger.info(f"Midway index: {midway_index}")

    # Get index of first occurence of *** in second half:
    star_index = input_text.find(STAR_SEPARATOR, midway_index)
    logger.info(f"Star index: {star_index}")

    return star_index


def split_file(file_name: str) -> Dict[str, Union[str, bool]]:
    """
    Read a file and split its content based on the '***' separator.

    Args:
        file_name (str): The name of the file to process.

    Returns:
        Dict[str, Union[str, bool]]: A dictionary containing:
            - 'first_half': The content before '***' (if found)
            - 'second_half': The content after '***' (if found)
            - 'no_stars': Boolean indicating if '***' was not found
            - 'full_text': The entire content of the file
            - 'ERROR': Error message if an exception occurred
    """
    try:
        with open(file_name, "r") as input_file:
            input_text = input_file.read()

        # Get index of first occurence of *** in second half:
        star_index = get_star_index(input_text)

        if star_index == -1:
            return {FULL_TEXT: input_text, NO_STARS: True}

        first_half = input_text[:star_index].strip()
        second_half = input_text[star_index + len(STAR_SEPARATOR) :].strip()

        ret_data: Dict[str, Union[str, bool]] = {
            FIRST_HALF: first_half,
            SECOND_HALF: second_half,
            NO_STARS: False,
            FULL_TEXT: input_text,
        }

        return ret_data
    except Exception as e:
        logger.error(f"Error processing file {file_name}: {str(e)}")
        return {"ERROR": str(e)}
