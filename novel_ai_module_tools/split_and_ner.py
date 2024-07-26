import logging
import sys
from pathlib import Path
from typing import List, Tuple

from numpy import random

from novel_ai_module_tools.config import *
from novel_ai_module_tools.ner import perform_ner
from novel_ai_module_tools.split_file import split_file

logger = logging.getLogger(__name__)


def create_directories(working_directory: Path) -> Tuple[Path, Path, Path]:
    """
    Create necessary directories for processing files.

    Args:
        working_directory (Path): The base working directory.

    Returns:
        Tuple[Path, Path, Path]: Paths to names_replaced, splits, and ner directories.
    """
    names_replaced_directory = working_directory / "names_replaced"
    splits_directory = names_replaced_directory / "splits"
    ner_directory = names_replaced_directory / "ner"

    for directory in [names_replaced_directory, splits_directory, ner_directory]:
        directory.mkdir(parents=True, exist_ok=True)

    return names_replaced_directory, splits_directory, ner_directory


def process_single_file(
    file_name: str, working_directory: Path, splits_directory: Path
) -> Path:
    """
    Process a single file by splitting it and saving the results.

    Args:
        file_name (str): Name of the file to process.
        working_directory (Path): Directory containing the files to process.
        splits_directory (Path): Directory to save split files.

    Returns:
        Path: Path to the processed file (either full file or randomly chosen split).
    """
    full_filename = working_directory / file_name
    splits = split_file(str(full_filename))
    logger.info(f"Splitting file: [{full_filename}]")

    if splits["no_stars"]:
        file_path = splits_directory / f"nosplits_{file_name}"
        file_path.write_text(splits["full_text"])
        return file_path
    else:
        first_half_file_path = (
            splits_directory / f"{SPLITS_FIRST_HALF_PREFIX}{file_name}"
        )
        second_half_file_path = (
            splits_directory / f"{SPLITS_SECOND_HALF_PREFIX}{file_name}"
        )

        first_half_file_path.write_text(splits["first_half"])
        second_half_file_path.write_text(splits["second_half"])

        return random.choice([first_half_file_path, second_half_file_path])


def process_files(working_directory: str) -> None:
    """
    Process all .txt files in the working directory by splitting them and performing NER.

    Args:
        working_directory (str): Path to the working directory containing files to process.
    """
    working_directory = Path(working_directory)
    resource_dir = Path(__file__).parent / "resources"
    names_replaced_directory, splits_directory, ner_directory = create_directories(
        working_directory
    )

    txt_filenames = [
        f.name
        for f in working_directory.iterdir()
        if f.is_file() and f.suffix == ".txt" and not f.name.startswith(".")
    ]

    logger.info(
        f"Splitting and performing NER on .txt files in directory: [{working_directory}]"
    )
    ner_source_files: List[Path] = [
        process_single_file(file_name, working_directory, splits_directory)
        for file_name in txt_filenames
    ]

    perform_ner(
        file_names=[str(f) for f in ner_source_files],
        ner_directory=str(ner_directory),
        resource_directory=str(resource_dir),
        strip_prefixes=[
            "nosplits_",
            SPLITS_FIRST_HALF_PREFIX,
            SPLITS_SECOND_HALF_PREFIX,
        ],
    )


if __name__ == "__main__":
    try:
        working_directory = sys.argv[1]
    except IndexError:
        print("Please pass directory name")
        sys.exit(1)

    process_files(working_directory)
