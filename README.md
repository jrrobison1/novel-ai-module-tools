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

### 3_split_and_ner.py

### 4_find_and_replace.py

### 5_construct_graphs.py


