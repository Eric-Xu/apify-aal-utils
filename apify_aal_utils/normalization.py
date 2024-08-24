import re

import usaddress

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
        "Scotch Plains Twp."
        "Roselle Park Boro"

    Outputs:
        "Scotch Plains"
        "Roselle Park"
    """
    city_temp = value
    for suffix in CITY_SUFFIXES:
        city_temp = re.sub(suffix, "", city_temp, flags=re.IGNORECASE)
        city_temp = re.sub(r"[^a-zA-Z-\s]", "", city_temp)
        city_temp = city_temp.strip()
    city_cleaned = " ".join(city_temp.split())
    return city_cleaned


def rm_zip_code_extension(value: str) -> str:
    """
    Converts a 9-digit ZIP Code into a 5-digit ZIP Code.

    Sample Inputs:
        "07005-9551"
        "07670"

    Outputs:
        "07005"
        "07670"
    """
    return value.replace(" ", "").split("-")[0]


def simple_address(value: str) -> str:
    """
    Removes city suffixes.
    Converts a 9-digit ZIP Code into 5 digits.

    Sample Inputs:
        "339 Split Rock Rd, Rockaway Twp., NJ 07005-9551"
        "95 Walnut Dr, Tenafly, NJ 07670"

    Outputs:
        "339 Split Rock Rd, Rockaway, NJ 07005"
        "95 Walnut Dr, Tenafly, NJ 07670"
    """
    result = ""
    address_components, address_type = usaddress.tag(value)
    if address_type == "Street Address":
        city_original: str = address_components["PlaceName"]
        city_cleaned: str = clean_city(city_original)
        zip_code_original: str = address_components["ZipCode"]
        zip_code_5_digit: str = rm_zip_code_extension(zip_code_original)
        result = value.replace(city_original, city_cleaned)
        result = result.replace(zip_code_original, zip_code_5_digit)
    return result
