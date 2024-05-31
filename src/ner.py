import os
import spacy
from config import *
from resources_loader import load_name_recognizers


def get_unique_entities(ner_entities):
    # Create a set to avoid duplicates
    entities = set()

    # Add only PERSON entities that start with an uppercase letter
    for word in ner_entities.ents:
        if word.label_ == "PERSON":
            for name in word.text.split():
                if name[0].isupper():
                    entities.add(name)

    return entities


def get_ner_write_file(ner_directory, file_name, strip_prefixes):
    base_file_name = os.path.basename(file_name)
    for strip_prefix in strip_prefixes:
        base_file_name = base_file_name.removeprefix(strip_prefix)

    return open(os.path.join(ner_directory, NER_FILE_PREFIX + base_file_name), "w")


def perform_ner(file_names, ner_directory, resource_directory, strip_prefixes):
    names = load_name_recognizers()

    # Ignore Names
    with open(os.path.join(resource_directory, "ignore_names.txt")) as f:
        ignore_names = f.read().splitlines()
    f.close()

    NER = spacy.load(
        NER_MODEL, disable=["tagger", "parser", "attribute_ruler", "lemmatizer"]
    )

    for file_name in file_names:
        with open(file_name, "r") as file:
            data = file.read()

        ner_entities = NER(data)
        unique_entities = get_unique_entities(ner_entities)
        output_file = get_ner_write_file(ner_directory, file_name, strip_prefixes)

        for name in sorted(unique_entities):
            if name[:-1] in unique_entities:  # Ignore plurals of the same name
                continue
            if (
                name.endswith("'s") or name.lower() in ignore_names
            ):  # Ignore possessives
                continue

            write_out = name + "|PERSON|"

            for name_type, name_list in names.items():
                if name in name_list:
                    write_out = write_out + name_type
                    break

            output_file.write(write_out + "\n")

        file.close()
        output_file.close()
