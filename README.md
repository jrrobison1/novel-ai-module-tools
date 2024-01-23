# novel-ai-module-tools
Series of tools for use in preparing text for AI module generation in NovelAI (https://novelai.net/). 

These are model-agnostic. I wrote them when Sigurd was the newest model, but they work fine formatting for Euterpe. The latest NovelAI model, Kayra, is great, but I don't know if allowing module creation for Kayra is on the NovelAI road map. If module creation for Kayra is added, these tools _should_ work, but I will revisit these if that were to happen.

## The tools
There are five tools, prefixed with the number in the order in which they should be run.

### 1_formatter.py
Formats the text in the way NovelAI likes. Each paragraph on a separate line. Fancy quotes into regular quotes. Smart ellipsis into simple txt version. Dashes replaced with em's. Simple section/chapter headings replaced with "***".

Formats all text files in the directory.

The directory passes to `1_formatter` is expected to have its txt files in a directory called `edited`. The files are modified in-place.

Run: `python 1_formatter.py <directory_name>`

### 2_match_count.py
Run: `python 2_match_count.py <file_name>`

### 3_split_and_ner.py
Run: `python 3_split_and_ner.py <directory_name>`

### 4_find_and_replace.py
Run: `python 4_find_and_replace.py <directory_name>`

### 5_construct_graphs.py
Run: `python 3_construct_graphs.py <directory_name>`


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
        "model": "en_core_web_trf"
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

`patterns["match_primary_score_first_threshold"]`:

`patterns[match_secondary_score_first_threshold"]`:

`patterns[match_primary_score_second_threshold"]`:

`patterns[match_secondary_score_second_threshold]"`:

`patterns[match_word_count_threshold]`:

`patterns[original_name_similarity_threshold"]`:

`patterns[used_name_in_project_similarity_threshold"]`:

`patterns[used_name_in_file_similarity_threshold"]`:
