import os
import re
import sys

from novel_ai_module_tools.logger_config import get_logger


logger = get_logger(__file__)

"""
formatter.py

This script processes text files in a specified directory, applying various formatting
rules to standardize and clean up the text content.

Usage:
    python formatter.py <directory_path>
    python formatter.py <file_path>

"""


def format_files():
    """
    Process and format text files in the specified directory or a single file.

    This function applies various text formatting rules to either all .txt files in a directory
    or a single file, depending on the input provided.

    Raises:
        SystemExit: If the path is not provided as a command-line argument.
        IOError: If there are issues reading from or writing to files.
    """
    try:
        input_path = sys.argv[1]
    except IndexError:
        print("Please pass a directory or file path")
        sys.exit(1)

    if os.path.isfile(input_path):
        process_file(input_path)
    elif os.path.isdir(input_path):
        filenames = [
            f
            for f in os.listdir(input_path)
            if f.endswith(".txt") and os.path.isfile(os.path.join(input_path, f))
        ]
        num_files = len(filenames)
        print(f"Found {num_files} .txt file(s) in the directory: {input_path}")
        confirmation = (
            input(f"Do you want to format {num_files} file(s)? (Y/n): ").strip().lower()
        )
        if confirmation in ["y", "yes", ""]:
            for file_name in filenames:
                full_filename = os.path.join(input_path, file_name)
                process_file(full_filename)
        else:
            logger.info("Format files in directory canceled by user.")
            print("Operation cancelled.")
            sys.exit(0)
    else:
        print(f"The provided path {input_path} is neither a file nor a directory")
        sys.exit(1)


def process_file(file_path):
    """
    Process and format a single text file.

    Args:
        file_path (str): The path to the file to be processed.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_text = f.read()

            # Replace fancy quotes with regular quotes
            source_text = re.sub(r"[“”]", '"', source_text)
            source_text = re.sub(r"[‘’`]", "'", source_text)

            # Replace different dash/hyphen patterns
            source_text = re.sub(r" --- ", " - ", source_text)  # Change to hyphen
            source_text = re.sub(r"---", "–", source_text)  # Change to en dash

            # Replace ellipsis variations with standard ellipsis
            source_text = re.sub(r"…|\s\.\s\.\s\.", "...", source_text)
            source_text = re.sub(r"\s\.\.\.", "...", source_text)

            # Standardize section/chapter markers
            source_text = re.sub(
                r"CHAPTER \d+$", "***", source_text, flags=re.MULTILINE
            )

            # Reduce multiple "***" lines to a single one
            source_text = re.sub(
                r"(^\*\*\*$\n){2,}", "***\n", source_text, flags=re.MULTILINE
            )

            # Replace multiple newlines with section separator
            source_text = re.sub(r"\n{3,}", "\n***\n", source_text)

            source_text = re.sub(r"\*{4,}", "***", source_text)

            # Remove empty lines
            source_text = re.sub(r"^\s*$", "", source_text, flags=re.MULTILINE)

            # Trim leading and trailing whitespace
            source_text = re.sub(r"^\s+|\s+$", "", source_text, flags=re.MULTILINE)

            # Remove lines with only digits
            source_text = re.sub(r"^\d+$", "", source_text, flags=re.MULTILINE)

            # Generate the new file name with "_fmtd" suffix
            file_name, file_extension = os.path.splitext(file_path)
            new_file_path = f"{file_name}_fmtd{file_extension}"

            # Write the formatted content to the new file
            with open(new_file_path, "w", encoding="utf-8") as f:
                f.write(source_text)

            logger.info(f"Formatted file saved as: {new_file_path}")

    except IOError as e:
        logger.error(f"Error processing file {file_path}: {e}")


if __name__ == "__main__":
    logger.debug("Beginning script.")
    format_files()
    logger.debug("Script complete.")
