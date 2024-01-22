#!/usr/bin/env python3
# Used to do preliminary formatting of source files
import os
import re
import sys
from os import walk

try:
    working_directory = sys.argv[1]
except:
    print("Please pass directory name")
    exit(1)


print("Beginning script...")
edited_directory = os.path.join(working_directory, "edited")
edited_filenames = next(walk(edited_directory), (None, None, []))[2]
for filename in edited_filenames:
    if (filename.startswith(".")):
        edited_filenames.remove(filename)

for file_name in edited_filenames:
    full_filename = os.path.join(edited_directory, file_name)
    with open(full_filename, "r") as f:
        source_text = f.read()
    f.close()

    source_text = re.sub(r"“|”", "\"", source_text, flags=re.MULTILINE)
    source_text = re.sub(r"‘|’|`", "'", source_text, flags=re.MULTILINE)
    source_text = re.sub(r" --- ", " – ", source_text, flags=re.MULTILINE)
    source_text = re.sub(r"---", "—", source_text, flags=re.MULTILINE)
    source_text = re.sub(r"…", "...", source_text, flags=re.MULTILINE)
    source_text = re.sub(r" \. \. \.", "...", source_text, flags=re.MULTILINE)
    source_text = re.sub(r" \.\.\.", "...", source_text, flags=re.MULTILINE)
    source_text = re.sub(r"\n\n\n", "\n***\n", source_text, flags=re.MULTILINE)
    source_text = re.sub(r"^CHAPTER \d+", "***", source_text, flags=re.MULTILINE)
    source_text = re.sub(r"\*{4,}", "***", source_text, flags=re.MULTILINE)
    source_text = re.sub(r"^\s+", "", source_text, flags=re.MULTILINE)
    source_text = re.sub(r"\s+$", "", source_text, flags=re.MULTILINE)
    source_text = re.sub(r"^\d+$", "", source_text, flags=re.MULTILINE)
    source_text = re.sub(r"(^\*\*\*$\n){2,}", "***\n", source_text, flags=re.MULTILINE)
    source_text = re.sub(r"^$", "", source_text, flags=re.MULTILINE)

    with open(full_filename, "w") as f:
        f.write(source_text)
    f.close()
