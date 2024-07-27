from typing import Dict, List, Set, TextIO
from pathlib import Path

import spacy
from spacy.language import Language
from spacy.tokens import Doc

from novel_ai_module_tools.config import *
from novel_ai_module_tools.resources_loader import load_name_recognizers


def get_unique_entities(ner_entities: Doc) -> Set[str]:
    """
    Extract unique PERSON entities from a spaCy Doc object.

    Args:
        ner_entities (Doc): A spaCy Doc object containing named entities.

    Returns:
        Set[str]: A set of unique person names that start with an uppercase letter.
    """
    entities: Set[str] = set()

    # Add only PERSON entities that start with an uppercase letter
    for word in ner_entities.ents:
        if word.label_ == "PERSON":
            for name in word.text.split():
                if name[0].isupper():
                    entities.add(name)

    return entities


def get_ner_write_file(
    ner_directory: Path, file_name: Path, strip_prefixes: List[str]
) -> Path:
    """
    Create a Path object for the NER results file.

    Args:
        ner_directory (Path): The directory where the output file will be created.
        file_name (Path): The original file path.
        strip_prefixes (List[str]): Prefixes to be removed from the file name.

    Returns:
        Path: A Path object for the NER results file.
    """
    base_file_name = file_name.name
    for strip_prefix in strip_prefixes:
        base_file_name = base_file_name.removeprefix(strip_prefix)

    return ner_directory / f"{NER_FILE_PREFIX}{base_file_name}"


def perform_ner(
    file_names: List[Path],
    ner_directory: Path,
    resource_directory: Path,
    strip_prefixes: List[str],
) -> None:
    """
    Perform Named Entity Recognition (NER) on a list of files and write the results.

    Args:
        file_names (List[Path]): List of file paths to process.
        ner_directory (Path): Directory to save the NER results.
        resource_directory (Path): Directory containing resource files.
        strip_prefixes (List[str]): Prefixes to be removed from output file names.

    Returns:
        None
    """
    names: Dict[str, List[str]] = load_name_recognizers()

    # Ignore Names
    try:
        logger.info(
            f"Loading ignore names from: [{resource_directory}/ignore_names.txt]"
        )
        ignore_names = (
            (resource_directory / "ignore_names.txt").read_text().splitlines()
        )
    except FileNotFoundError:
        ignore_names = []

    logger.info(f"Loading NER model: [{NER_MODEL}]")
    NER: Language = spacy.load(
        NER_MODEL, disable=["tagger", "parser", "attribute_ruler", "lemmatizer"]
    )

    for file_name in file_names:
        data: str = file_name.read_text()

        ner_entities: Doc = NER(data)
        unique_entities: Set[str] = get_unique_entities(ner_entities)
        logger.info(
            f"Found {len(unique_entities)} unique entities in file: [{file_name}]"
        )

        output_file_path: Path = get_ner_write_file(
            ner_directory, file_name, strip_prefixes
        )

        with output_file_path.open("w") as output_file:
            number_of_plurals = 0
            number_of_possessives = 0
            number_of_ignored = 0
            for name in sorted(unique_entities):
                if name[:-1] in unique_entities:  # Ignore plurals of the same name
                    number_of_plurals += 1
                    continue
                if name.endswith("'s"):
                    # Ignore possessives
                    number_of_possessives += 1
                    continue
                if name.lower() in ignore_names:
                    number_of_ignored += 1
                    continue

                write_out = f"{name}|PERSON|"

                for name_type, name_list in names.items():
                    if name in name_list:
                        write_out = write_out + name_type
                        break

                output_file.write(write_out + "\n")

        logger.info(
            f"Processed file: [{file_name}]. Skipped {number_of_plurals} plurals, {number_of_possessives} possessives, and {number_of_ignored} names from the ignore list."
        )
