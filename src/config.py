import json
import logging

logger = logging.getLogger("config")

CONFIG_FILE_NAME = "contentConfig.json"
DEFAULT_FIRST_HALF_PREFIX = "1h_"
DEFAULT_SECOND_HALF_PREFIX = "2h_"
DEFAULT_NER_FILE_PREFIX = "ner_"
DEFAULT_REPLACEMENTS_FILE_PREFIX = "replaced_"
DEFAULT_STITCHED_PREFIX = "stitched_"
DEFAULT_NER_MODEL = "en_core_web_sm"
DEFAULT_PRIMARY_PATTERN = "\sthis\s"
DEFAULT_SECONDARY_PATTERN = "\sexample\s"
DEFAULT_PRIMARY_SCORE_FIRST_THRESHOLD = 2
DEFAULT_SECONDARY_SCORE_FIRST_THRESHOLD = 15
DEFAULT_PRIMARY_SCORE_SECOND_THRESHOLD = 1
DEFAULT_SECONDARY_SCORE_SECOND_THRESHOLD = 20
DEFAULT_MATCH_WORD_COUND_THRESHOLD = 5
DEFAULT_ORIGINAL_NAME_SIMILARITY_THRESHOLD = 0.90
DEFAULT_USED_NAME_IN_PROJECT_SIMILARITY_THRESHOLD = 0.85
DEFAULT_USED_NAME_IN_FILE_SIMILARITY_THRESHOLD = 0.85
DEFAULT_LOG_LEVEL = "INFO"


config = {}

try:
    with open(CONFIG_FILE_NAME) as f:
        config = json.load(f)
    f.close()
except:
    logger.warning(
        f"No {CONFIG_FILE_NAME} config file found. " f"Will use only default values"
    )

try:
    SPLITS_FIRST_HALF_PREFIX = config["splits"]["first_half_prefix"]
except:
    logger.warning(
        f"No config value found for SPLITS_FIRST_HALF_PREFIX. "
        f"Using default value of [{DEFAULT_FIRST_HALF_PREFIX}]"
    )
    SPLITS_FIRST_HALF_PREFIX = DEFAULT_FIRST_HALF_PREFIX

try:
    SPLITS_SECOND_HALF_PREFIX = config["splits"]["second_half_prefix"]
except:
    logger.warning(
        f"No config value found for SPLITS_SECOND_HALF_PREFIX. "
        f"Using default value of [{DEFAULT_SECOND_HALF_PREFIX}]"
    )
    SPLITS_SECOND_HALF_PREFIX = DEFAULT_SECOND_HALF_PREFIX

try:
    NER_FILE_PREFIX = config["ner"]["file_prefix"]
except:
    logger.warning(
        f"No config value found for NER_FILE_PREFIX. "
        f"Using default value of [{DEFAULT_NER_FILE_PREFIX}]"
    )
    NER_FILE_PREFIX = DEFAULT_NER_FILE_PREFIX

try:
    REPLACEMENTS_FILE_PREFIX = config["replacements"]["replaced_prefix"]
except:
    logger.warning(
        f"No config value found for REPLACEMENTS_FILE_PREFIX. "
        f"Using default value of [{DEFAULT_REPLACEMENTS_FILE_PREFIX}]"
    )
    REPLACEMENTS_FILE_PREFIX = DEFAULT_REPLACEMENTS_FILE_PREFIX

try:
    NER_MODEL = config["ner"]["model"]
except:
    logger.warning(
        f"No config value found for REPLACEMENTS_FILE_PREFIX. "
        f"Using default value of [{DEFAULT_NER_MODEL}]"
    )
    NER_MODEL = DEFAULT_NER_MODEL

try:
    STITCHED_FILE_PREFIX = config["replacements"]["stitched_prefix"]
except:
    logger.warning(
        f"No config value found for STITCHED_FILE_PREFIX. "
        f"Using default value of [{DEFAULT_STITCHED_PREFIX}]"
    )
    STITCHED_FILE_PREFIX = DEFAULT_STITCHED_PREFIX

try:
    PRIMARY_PATTERN = config["patterns"]["primary"]
except:
    logger.warning(
        f"No config value found for PRIMARY_PREFIX. "
        f"Using default value of [{DEFAULT_PRIMARY_PATTERN}]"
    )
    PRIMARY_PATTERN = DEFAULT_PRIMARY_PATTERN

try:
    SECONDARY_PATTERN = config["patterns"]["secondary"]
except:
    logger.warning(
        f"No config value found for PRIMARY_PREFIX. "
        f"Using default value of [{DEFAULT_SECONDARY_PATTERN}]"
    )
    SECONDARY_PATTERN = DEFAULT_SECONDARY_PATTERN

try:
    PRIMARY_SCORE_FIRST_THRESHOLD = config["patterns"][
        "match_primary_score_first_threshold"
    ]
except:
    logger.warning(
        f"No config value found for PRIMARY_SCORE_FIRST_THRESHOLD. "
        f"Using default value of [{DEFAULT_PRIMARY_SCORE_FIRST_THRESHOLD}]"
    )
    PRIMARY_SCORE_FIRST_THRESHOLD = DEFAULT_PRIMARY_SCORE_FIRST_THRESHOLD

try:
    SECONDARY_SCORE_FIRST_THRESHOLD = config["patterns"][
        "match_secondary_score_first_threshold"
    ]
except:
    logger.warning(
        f"No config value found for SECONDARY_SCORE_FIRST_THRESHOLD. "
        f"Using default value of [{DEFAULT_SECONDARY_SCORE_FIRST_THRESHOLD}]"
    )
    SECONDARY_SCORE_FIRST_THRESHOLD = DEFAULT_SECONDARY_SCORE_FIRST_THRESHOLD

try:
    PRIMARY_SCORE_SECOND_THRESHOLD = config["patterns"][
        "match_primary_score_second_threshold"
    ]
except:
    logger.warning(
        f"No config value found for PRIMARY_SCORE_SECOND_THRESHOLD. "
        f"Using default value of [{DEFAULT_PRIMARY_SCORE_SECOND_THRESHOLD}]"
    )
    PRIMARY_SCORE_SECOND_THRESHOLD = DEFAULT_PRIMARY_SCORE_SECOND_THRESHOLD

try:
    SECONDARY_SCORE_SECOND_THRESHOLD = config["patterns"][
        "match_secondary_score_second_threshold"
    ]
except:
    logger.warning(
        f"No config value found for SECONDARY_SCORE_SECOND_THRESHOLD. "
        f"Using default value of [{DEFAULT_SECONDARY_SCORE_SECOND_THRESHOLD}]"
    )
    SECONDARY_SCORE_SECOND_THRESHOLD = DEFAULT_SECONDARY_SCORE_SECOND_THRESHOLD

try:
    MATCH_WORD_COUND_THRESHOLD = config["patterns"]["match_word_count_threshold"]
except:
    logger.warning(
        f"No config value found for MATCH_WORD_COUND_THRESHOLD. "
        f"Using default value of [{DEFAULT_MATCH_WORD_COUND_THRESHOLD}]"
    )
    MATCH_WORD_COUND_THRESHOLD = DEFAULT_MATCH_WORD_COUND_THRESHOLD

try:
    ORIGINAL_NAME_SIMILARITY_THRESHOLD = config["patterns"][
        "original_name_similarity_threshold"
    ]
except:
    logger.warning(
        f"No config value found for ORIGINAL_NAME_SIMILARITY_THRESHOLD. "
        f"Using default value of [{DEFAULT_ORIGINAL_NAME_SIMILARITY_THRESHOLD}]"
    )
    ORIGINAL_NAME_SIMILARITY_THRESHOLD = DEFAULT_ORIGINAL_NAME_SIMILARITY_THRESHOLD

try:
    USED_NAME_IN_PROJECT_SIMILARITY_THRESHOLD = config["patterns"][
        "used_name_in_project_similarity_threshold"
    ]
except:
    logger.warning(
        f"No config value found for USED_NAME_IN_PROJECT_SIMILARITY_THRESHOLD. "
        f"Using default value of [{DEFAULT_USED_NAME_IN_PROJECT_SIMILARITY_THRESHOLD}]"
    )
    USED_NAME_IN_PROJECT_SIMILARITY_THRESHOLD = (
        DEFAULT_USED_NAME_IN_PROJECT_SIMILARITY_THRESHOLD
    )

try:
    USED_NAME_IN_FILE_SIMILARITY_THRESHOLD = config["patterns"][
        "used_name_in_file_similarity_threshold"
    ]
except:
    logger.warning(
        f"No config value found for USED_NAME_IN_FILE_SIMILARITY_THRESHOLD. "
        f"Using default value of [{DEFAULT_USED_NAME_IN_FILE_SIMILARITY_THRESHOLD}]"
    )
    USED_NAME_IN_FILE_SIMILARITY_THRESHOLD = (
        DEFAULT_USED_NAME_IN_FILE_SIMILARITY_THRESHOLD
    )

try:
    LOG_LEVEL = config["logger"]["level"]
except:
    logger.warning(
        f"No config value found for LOG_LEVEL. "
        f"Using default value of [{DEFAULT_LOG_LEVEL}]"
    )
    LOG_LEVEL = DEFAULT_LOG_LEVEL
