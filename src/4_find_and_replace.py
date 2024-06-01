#!/usr/bin/env python3
import coloredlogs, logging
from config import *
from difflib import SequenceMatcher
import os
from os import replace, walk
from resources_loader import load_name_replacements
import random
import re
import sys


coloredlogs.install(level=LOG_LEVEL, fmt="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

try:
    working_directory = sys.argv[1]
except:
    print("Please pass directory name")
    exit(1)


names = load_name_replacements()
original_character_names = set()

resource_directory = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "resources"
)

# Last names ending in s
try:
    with open(os.path.join(resource_directory, "surnames_ending_s.txt")) as f:
        surnames_ending_s = f.read().splitlines()
        random.shuffle(surnames_ending_s)
    f.close()
except:
    surnames_ending_s = []

# Last names ending in x
try:
    with open(os.path.join(resource_directory, "surnames_ending_x.txt")) as f:
        surnames_ending_x = f.read().splitlines()
        random.shuffle(surnames_ending_x)
    f.close()
except:
    surnames_ending_x = []

# Top level names replacement directory
names_replaced_directory = os.path.join(working_directory, "names_replaced")

# Location of files to be split in two
splits_directory = os.path.join(names_replaced_directory, "splits")

# Location where the ner files are put
ner_directory = os.path.join(names_replaced_directory, "ner")

output_directory = os.path.join(names_replaced_directory, "replaced")
os.makedirs(output_directory, exist_ok=True)

# Get file list
file_names = next(walk(splits_directory), (None, None, []))[2]  # [] if no file
for filename in file_names:
    if filename.startswith("."):
        file_names.remove(filename)


def get_unique_replacement(
    original_name, name_type, replacement_list, used_project_pile, used_file_pile
):
    for candidate in replacement_list:
        fail = False

        # Replace last names ending with 's' or 'x' with names that also end in 's' or 'x'
        if (
            name_type.startswith("S")
            and (original_name.endswith("s") or original_name.endswith("x"))
            and not (candidate.endswith("s") or candidate.endswith("x"))
        ):
            logger.info(
                f"Unable to use candidate [{candidate}] for original name [{original_name}] because the replacement does not end with 's' or 'x'"
            )
            continue
        if (
            name_type.startswith("S")
            and (candidate.endswith("s") or candidate.endswith("x"))
            and not (original_name.endswith("s") or original_name.endswith("x"))
        ):
            logger.info(
                f"Unable to use candidate [{candidate}] for original name [{original_name}] because the original name does not end with 's' or 'x'"
            )
            continue

        # Was the this candidate replacement used in the original text?
        for used_name in original_character_names:
            similarity = SequenceMatcher(None, candidate, used_name).ratio()
            if similarity > ORIGINAL_NAME_SIMILARITY_THRESHOLD:
                logger.info(
                    f"Unable to replace [{original_name}] with [{candidate}] because it is too similar to [{used_name}] which was already an ORIGINAL character name for the project. Similarity is [{similarity}]"
                )
                fail = True
                break
        if fail == True:
            replacement_list.remove(candidate)
            continue

        # Have we already used a similar replacement elsewhere in the project?
        for used_name in used_project_pile:
            similarity = SequenceMatcher(None, candidate, used_name).ratio()
            if similarity > USED_NAME_IN_PROJECT_SIMILARITY_THRESHOLD:
                logger.info(
                    f"Unable to replace [{original_name}] with [{candidate}] because it is too similar to [{used_name}] which is already in the PROJECT list. Similarity is [{similarity}]"
                )
                fail = True
                break
        if fail == True:
            replacement_list.remove(candidate)
            continue

        # Have we already used a similar replacement within this file?
        for used_name in used_file_pile:
            similarity = SequenceMatcher(None, candidate, used_name).ratio()
            if similarity > USED_NAME_IN_FILE_SIMILARITY_THRESHOLD:
                logger.info(
                    f"Unable to replace [{original_name}] with [{candidate}] because it is too similar to [{used_name}] which is already in the FILE list. Similarity is [{similarity}]"
                )
                fail = True
                break

        replacement_list.remove(candidate)
        if fail == False:
            logger.debug(
                f"Candidate not found in existing list. Returning candidate [{candidate}]"
            )
            return candidate

    logger.debug(
        f"Returning EMPTY from get_unique_replacement. Original name [{original_name}] Replacement list size [{len(replacement_list)}]"
    )
    return ""


def get_replacement(original_name, name_type, used_project_pile, used_file_pile):
    for category, replacement_list in names.items():
        if name_type == category:
            return get_unique_replacement(
                original_name,
                name_type,
                replacement_list,
                used_project_pile,
                used_file_pile,
            )

    logger.debug(f"Returning EMPTY because the name_type never mathced the category")
    return ""


def get_ner_file_text(file_name, strip_prefixes):
    base_file_name = os.path.basename(file_name)
    for strip_prefix in strip_prefixes:
        base_file_name = base_file_name.removeprefix(strip_prefix)

    with open(
        os.path.join(ner_directory, NER_FILE_PREFIX + base_file_name), "r"
    ) as ner_file:
        replacements = ner_file.read()
    ner_file.close()

    return replacements


def get_input_text(file_name):
    with open(os.path.join(splits_directory, file_name), "r") as input_file:
        input_text = input_file.read()
    input_file.close()

    return input_text


for file_name in file_names:
    ner_file_text = get_ner_file_text(
        file_name, ["nosplits_", SPLITS_FIRST_HALF_PREFIX, SPLITS_SECOND_HALF_PREFIX]
    )
    ner_lines = ner_file_text.splitlines()

    for ner_line in ner_lines:
        original_name, __, name_type = ner_line.split("|")
        original_character_names.add(original_name)


for file_name in file_names:
    used_project_pile = []
    used_file_pile = []
    input_text = get_input_text(file_name)
    ner_file_text = get_ner_file_text(
        file_name, ["nosplits_", SPLITS_FIRST_HALF_PREFIX, SPLITS_SECOND_HALF_PREFIX]
    )

    ner_lines = ner_file_text.splitlines()

    for ner_line in ner_lines:
        logger.info(f"Processing line: [{ner_line}]")
        original_name, __, name_type = ner_line.split("|")

        if name_type == "":
            logger.error(
                f"{file_name} ERROR Unable to make replacement for string: [{original_name}] because no name type was given for this line"
            )
            continue
        else:
            replacement = get_replacement(
                original_name, name_type, used_project_pile, used_file_pile
            )

            if replacement == "":
                logger.error(
                    f"{file_name} ERROR Unable to make replacement for string: [{original_name}] because the replacement is EMPTY"
                )
                continue
            used_project_pile.append(replacement)
            used_file_pile.append(replacement)
            input_text = re.sub(
                r"(^|[ ?!,.();'\"\-–—])%s([ ?!,.();'\"\-–—])"
                % re.escape(original_name),
                r"\1%s\2" % re.escape(str.strip(replacement)),
                input_text,
                flags=re.MULTILINE,
            )
            logger.info(
                f"{filename}: Successfully replaced string [{original_name}] with string [{replacement}]"
            )

    replaced_file = open(
        os.path.join(output_directory, REPLACEMENTS_FILE_PREFIX + file_name), "w"
    )
    replaced_file.write(input_text)
    replaced_file.close()

# Now stitch the resulting files together
stitched_directory = os.path.join(names_replaced_directory, "stitched")
os.makedirs(stitched_directory, exist_ok=True)

for file_name in file_names:
    base_name = file_name.removeprefix(SPLITS_FIRST_HALF_PREFIX).removeprefix(
        SPLITS_SECOND_HALF_PREFIX
    )

    if base_name.startswith("nosplits_"):
        # Open first half
        with open(
            os.path.join(output_directory, REPLACEMENTS_FILE_PREFIX + base_name), "r"
        ) as input_file:
            full_text = input_file.read()
            input_file.close()
        # Open stitched file for output
        with open(
            os.path.join(
                stitched_directory,
                STITCHED_FILE_PREFIX + base_name.removeprefix("nosplits_"),
            ),
            "w",
        ) as stitched_write_file:
            stitched_write_file.write(full_text)
            stitched_write_file.close()
    else:
        # Open first half
        with open(
            os.path.join(
                output_directory,
                REPLACEMENTS_FILE_PREFIX + SPLITS_FIRST_HALF_PREFIX + base_name,
            ),
            "r",
        ) as input_file:
            first_half = input_file.read()
            input_file.close()

        # Open second half
        with open(
            os.path.join(
                output_directory,
                REPLACEMENTS_FILE_PREFIX + SPLITS_SECOND_HALF_PREFIX + base_name,
            ),
            "r",
        ) as input_file:
            second_half = input_file.read()
            input_file.close()

        stitched = first_half + "\n***\n" + second_half

        # Open stitched file for output
        with open(
            os.path.join(stitched_directory, STITCHED_FILE_PREFIX + base_name), "w"
        ) as stitched_write_file:
            stitched_write_file.write(stitched)
            stitched_write_file.close()
