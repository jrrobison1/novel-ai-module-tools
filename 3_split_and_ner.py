#!/usr/bin/env python3
import os
import sys
from os import walk

from numpy import random

from ner import perform_ner
from split_file import splitFile
from config import *


try:
    working_directory = sys.argv[1]
except:
    print("Please pass directory name")
    exit(1)


resource_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")

# Edited files
edited_directory = os.path.join(working_directory, "edited")

# Top level names replacement directory
names_replaced_directory = os.path.join(working_directory, "names_replaced")
os.makedirs(names_replaced_directory, exist_ok=True)

# Location of files to be split in two
splits_directory = os.path.join(names_replaced_directory, "splits")
os.makedirs(splits_directory, exist_ok=True)

# Location where the ner files are put
ner_directory = os.path.join(names_replaced_directory, "ner")
os.makedirs(ner_directory, exist_ok=True)

# Get edited file list
edited_filenames = next(walk(edited_directory), (None, None, []))[2]
for filename in edited_filenames:
    if (filename.startswith(".")):
        edited_filenames.remove(filename)

ner_source_files = []

# Create splits
for file_name in edited_filenames:
    full_filename = os.path.join(edited_directory, file_name)
    splits = splitFile(full_filename)

    if splits["no_stars"] == True:
        no_splits_file = open(os.path.join(splits_directory, "nosplits_" + file_name), "w")
        no_splits_file.write(splits["full_text"])
        no_splits_file.close()

        print(f"Will perform NER on file: [{no_splits_file.name}]")
        ner_source_files.append(no_splits_file.name)

    else:
        first_half_file = open(os.path.join(splits_directory, SPLITS_FIRST_HALF_PREFIX + file_name), "w")
        first_half_file.write(splits["first_half"])
        first_half_file.close()

        second_half_file = open(os.path.join(splits_directory, SPLITS_SECOND_HALF_PREFIX + file_name), "w")
        second_half_file.write(splits["second_half"])
        second_half_file.close()

        random_choice = random.choice([first_half_file.name, second_half_file.name])
        print(f"Will perform NER on file: [{random_choice}]")
        ner_source_files.append(random_choice)

perform_ner(ner_source_files, ner_directory, resource_dir, ["nosplits_", SPLITS_FIRST_HALF_PREFIX, SPLITS_SECOND_HALF_PREFIX])
