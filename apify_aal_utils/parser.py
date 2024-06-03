def n_chars_around(
    phrase: str, word: str, n: int = 50, ignore_case: bool = True
) -> str:
    """Return a snippet of text n characters around the search word.

    phrase = "The quick brown fox jumps over the lazy dog."
    >>> n_chars_around(phrase, "fox", 10)
    'ick brown fox jumps ove'
    """
    length: int = len(word)
    if ignore_case:
        first_char_idx: int = phrase.lower().find(word.lower())
    else:
        first_char_idx: int = phrase.find(word)
    start = first_char_idx - n if first_char_idx - n > 0 else 0
    end = first_char_idx + length + n
    extracted = phrase[start:end]
    return extracted
