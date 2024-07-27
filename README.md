# novel-ai-module-tools
[![CI](https://github.com/jrrobison1/novel-ai-module-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/jrrobison1/novel-ai-module-tools/actions/workflows/ci.yml) 
Series of tools for preparing text for AI module generation in NovelAI (https://novelai.net/).

These tools are model-agnostic. They were originally written for the Sigurd model but work fine for formatting Euterpe modules as well. The latest NovelAI model, Kayra, is great, but module creation for Kayra is not currently available. If module creation for Kayra is added in the future, these tools _should_ work, but they will be revisited if necessary.

## Installation
This project uses Poetry for dependency management.
1. Ensure `poetry` is installed:
    - `pip install poetry`
2. Clone this repository
3. Within the project directory, run `poetry install`

Alternatively, you can use the included `requirements.txt` file:
```
pip install -r requirements.txt
```

## The tools
### 1. formatter.py
Formats text in the way NovelAI prefers:
- Each paragraph on a separate line
- Fancy quotes converted to regular quotes
- Smart ellipsis converted to simple text version
- Dashes replaced with em dashes
- Simple section/chapter headings replaced with "***"

Usage:
```
poetry run python formatter.py <file_name>
poetry run python formatter.py <directory_name>
```
or
```
python formatter.py <file_name>
python formatter.py <directory_name>
```

Formats the provided file or all .txt files in the directory. Formatted files are saved with an "_fmtd" suffix.

NOTE: Running on a directory will format _all_ .txt files in that directory.

### 2. pick_and_choose.py
Usage: 
```
poetry run python pick_and_choose.py <file_name> <output_file_name>
```
poetry run python pick_and_choose.py <file_name> <output_file_name>
```
or
```
python pick_and_choose.py <file_name> <output_file_name>
```

GUI application (using Qt) to select and modify sections of text for module creation. Statistics are calculated and a graph is displayed based on regular expression patterns defined in contentConfig.json.

To see relevant graphs in the GUI, modify the "patterns"->"primary" and "secondary" values in contentConfig.json to match your desired regular expressions.

![Pick and Choose Screenshot](/img/2_screenshot.png "Pick and Choose Screenshot")

### 3. split_and_ner.py
Usage: 
```
poetry run python split_and_ner.py <directory_name>
```
or
```
python split_and_ner.py <directory_name>
```

Splits files in the given directory in half and performs Named Entity Recognition (NER) on each half using spaCy. This helps prevent over-focusing on specific names in the training text.

Modules have a tendency to make NovelAI over-focus on specific names present in your training text. For example, if the text
contains the name "Carlos", you will notice while using the module in NovelAI that a characters named Carlos frequently enter your stories at random. You can avoid this by splitting the text up, and replacing the original names with different names.

This script splits the files in the given directory in half, evenly on the "***" separator. It performs NER separately on each half (using spaCy), creating both the split files and files containing lists of named entities.

This script will create subdirectories within the directory specified:
```
- names_replaced
   - ner
       For each original file:
       - ner_<original_file_name>
   - splits
       For each original file:
       - 1h_<original_file_name> <- First half of original file
       - 2h_<original_file_name> <- Second half of original file
```

##### The ner_<original_file_name> files
You will see in the file something like this:
```
Aikam|PERSON|
Andrew|PERSON|M
Ashil|PERSON|
Besźel|PERSON|
Boatman|PERSON|
Boats|PERSON|
Brandi|PERSON|F
Brubaker|PERSON|
Buidze|PERSON|
Callahan|PERSON|M
Cameron|PERSON|F
```

Each line is formatted: 
`<entity name found in text>|<type of named entity>|<type of name>`

In the above example, `<type of name>` was detected as a male name for "Andrew" and female name for "Brandi"

To detect the `<type of name>`, names found in `resources->names->recognize` are used. This repository provides "F", "M" and "S" name lists, corrersponding to common male, female, and surnames. 

However, you may customize this however you like. You may create your own name lists—whatever file name you create will be used by the script to determine the `<type of name>`. For example, if you create a list named `gender_neutral.txt`, named entities found in your list will show up, for example, like `Sam|PERSON|gender_neutral`

If the name found through NER was not found in one of your name lists, the line for that named entity in the ner file will have nothing after the final pipe symbol. It is recommended for these cases to manually edit the ner file to include the name type; for example you might change `Buidze|PERSON|` to `Buidze|PERSON|S`.

This becomes important when running the next tool (`find_and_replace.py`)


### 4. find_and_replace.py
Usage: 
```
poetry run python find_and_replace.py <directory_name>
```
or
```
python find_and_replace.py <directory_name>
```

Expects `split_and_ner` to have been run.

`find_and_replace.py` uses the list of named entities that were found by `split_and_ner.py` and replaces those names with names you provide in `resources->names->replace` The text file in the `recognize` directory must be named the same as the text file in the `replace` directory. _However_, the lists themselves may be completely different. 

This allows many creative use cases. You may want to modify the names in the text to be more global. For example, if a text contains names that are typically used only in the U.S., you could use this to modify those names automatically with a list of more diverse names that you specify in a list. Alternatively, you may wish maintain the existing diversity of names in the text but still use different names. Or you may wish to make all names gender-neutral. Or replace all names with fantasy or sci-fi sounding names. Play around with this!

The result of running this script will be new files in the`<names_replaced>/<replaced>` subdirectory that have been split in half, had their named entities replaced, and have been stitched back together.

### 5. construct_graphs.py
Usage: 
```
poetry run python construct_graphs.py <directory_name>
```
or
```
python construct_graphs.py <directory_name>
```


## Configuration options
Configuration for the tools can be added in `contentConfig.json` in the base directory of your text.

An example using all available configurable options follows:
```{
    "splits": {
        "first_half_prefix": "1h_",
        "second_half_prefix": "2h_"
    },
    "ner": {
        "file_prefix": "ner_",
        "model": "en_core_web_sm"
    },
    "replacements": {
        "replaced_prefix": "replaced_",
        "stitched_prefix": "stitched_"
    }
    "patterns": {
        "primary": "\w",
        "secondary": "\w",
        "match_primary_score_first_threshold": "2",
        "match_secondary_score_first_threshold": "15",
        "match_primary_score_second_threshold": "1",
        "match_secondary_score_second_threshold": "20",
        "match_word_count_threshold": "5",
        "original_name_similarity_threshold": "0.90",
        "used_name_in_project_similarity_threshold": "0.8",
        "used_name_in_file_similarity_threshold": "0.85",
    }
    "logger" {
        "level": "INFO"
    }
}
```

### Configuration option descriptions
`first_half_prefix`: When files are split in half, the prefix to use for the file name of the first half of the split. This isn't an option that will normally need configuring.
Default: `1h_`

`second_half_prefix`: When files are split in half, the prefix to use for the file name of the second half of the split. This isn't an option that will normally need configuring.
Default: `2h_`

`file_prefix`: Prefix to use for files created by NER (Named Entity Recognition). The NER files created by this program are text files containing lists of entities recognized by Spacey.

You should not normally need to configure this file prefix yourself. Default: `ner_`

`model`: The spaCy model to use for NER. Take a look at the available models to use here: https://spacy.io/models/en. The larger models are more accurate but take longer to run. In my experience with using models in this program, the `en_core_web_sm` works well and is fast. However, the name list will need review and pruning afterwords. You might want to tinker with this to find the right balance of speed and accuracy for you.
Default: `en_core_web_sm`

`replaced_prefix`: When names from the text are replaced, the prefix used for the resulting file. There should normally be no need for configuring this manually.
Default: `replaced_`

`stitched_prefix`: The prefix to use for split files after they have been stitched back together. There should normally be no need for configuring this manually.
Default: `stitched_`

`patterns["primary"]`: For use in `2_match_count.py`. The primary pattern used to find sections of the text that match a particular regex.
Default: `\w`

`patterns["secondary"]`: For use in `2_match_count.py`. The secondary pattern used to find sections of the text that match a particular regex. Useful if there are two different patterns that one wishes to track separately
Default: `\w`
