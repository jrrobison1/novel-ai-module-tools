import logging
import os
import re
import sys
from os import walk

logger = logging.getLogger(__name__)

"""
1_formatter.py

This script processes text files in a specified directory, applying various formatting
rules to standardize and clean up the text content.

Usage:
    python 1_formatter.py <directory_path>

The script expects an 'edited' subdirectory within the specified directory,
containing the files to be processed.
"""

import logging
import os
import re
import sys
from os import walk

logger = logging.getLogger(__name__)


def format_files():
    """
    Process and format text files in the specified directory.

    This function applies various text formatting rules, including:
    - Replacing fancy quotes with regular quotes
    - Standardizing dashes and hyphens
    - Normalizing ellipsis usage
    - Replacing multiple newlines with section separators
    - Standardizing section/chapter markers
    - Trimming whitespace and removing empty lines
    - Removing lines with only digits

    The function reads files from the 'edited' subdirectory of the specified
    working directory, processes them, and writes the formatted content back
    to the same files.

    Raises:
        SystemExit: If the directory path is not provided as a command-line argument.
        IOError: If there are issues reading from or writing to files.
    """
    try:
        working_directory = sys.argv[1]
    except IndexError:
        print("Please pass directory name")
        sys.exit(1)

    edited_directory = os.path.join(working_directory, "edited")
    edited_filenames = [f for f in os.listdir(edited_directory) 
                        if not f.startswith('.') and os.path.isfile(os.path.join(edited_directory, f))]

    for file_name in edited_filenames:
        full_filename = os.path.join(edited_directory, file_name)
        try:
            with open(full_filename, "r", encoding="utf-8") as f:
                source_text = f.read()

            # Replace fancy quotes with regular quotes
            source_text = re.sub(r"[“”]", '"', source_text)
            source_text = re.sub(r"[‘’`]", "'", source_text)

            # Replace different dash/hyphen patterns
            source_text = re.sub(r" --- ", " – ", source_text)
            source_text = re.sub(r"---", "—", source_text)

            # Replace ellipsis variations with standard ellipsis
            source_text = re.sub(r"…|\s\.\s\.\s\.", "...", source_text)
            source_text = re.sub(r"\s\.\.\.", "...", source_text)

            # Replace multiple newlines with section separator
            source_text = re.sub(r"\n{3,}", "\n***\n", source_text)

            # Standardize section/chapter markers
            source_text = re.sub(r"^CHAPTER \d+", "***", source_text, flags=re.MULTILINE)
            source_text = re.sub(r"\*{4,}", "***", source_text)

            # Trim leading and trailing whitespace
            source_text = re.sub(r"^\s+|\s+$", "", source_text, flags=re.MULTILINE)

            # Remove lines with only digits
            source_text = re.sub(r"^\d+$", "", source_text, flags=re.MULTILINE)

            # Reduce multiple "***" lines to a single one
            source_text = re.sub(
                r"(^\*\*\*$\n){2,}", "***\n", source_text, flags=re.MULTILINE
            )

            # Remove empty lines
            source_text = re.sub(r"^\s*$", "", source_text, flags=re.MULTILINE)

            with open(full_filename, "w", encoding="utf-8") as f:
                f.write(source_text)

        except IOError as e:
            logger.error(f"Error processing file {full_filename}: {e}")


if __name__ == "__main__":
    logger.info("Running script...")
    format_files()
    print("Script complete.")
