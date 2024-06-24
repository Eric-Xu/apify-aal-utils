import re

from .constants import CITY_SUFFIXES


def safe_filename_component(value: str) -> str:
    """
    Normalize a string to be used as part of a filename.

    Sample Inputs:
        "100 Graham Ter Saddle Brook, NJ 07663",
        "15 SENECA TRAIL Denville Twp., NJ 07834-1421",
        "    410 E 5th Ave, Roselle Boro,     NJ ",

    Outputs:
        "100-graham-ter-saddle-brook-nj-07663",
        "15-seneca-trail-denville-twp-nj-07834-1421",
        "410-e-5th-ave-roselle-boro-nj",
    """
    result: str = value.strip()
    # Regex Property Description:
    # [] -- indicates a set of chars or a range.
    # ^ -- at the start of a square-bracket set inverts it.
    # \s -- (lowercase s) matches a single whitespace character.
    # + -- 1 or more occurrences of the pattern to its left.
    result: str = re.sub(r"[^0-9a-zA-Z-\s]", "", result)
    result: str = re.sub(r"  +", " ", result)
    result: str = result.replace(" ", "-").lower()
    return result


def clean_city(value: str) -> str:
    """
    City suffixes must be removed in order to be used as search terms in
    the Zillow Search API.

    Sample Inputs:
        "Scotch Plains Twp., NJ"
        "Roselle Park Boro, NJ"

    Outputs:
        "Scotch Plains, NJ"
        "Roselle Park, NJ"
    """
    city_temp = value
    for suffix in CITY_SUFFIXES:
        city_temp = re.sub(suffix, "", city_temp, flags=re.IGNORECASE)
    city_cleaned = " ".join(city_temp.split())
    return city_cleaned
