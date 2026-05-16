import re


def clean_text(text):

    if text is None:
        return ""

    text = str(text)

    # REMOVE EXTRA WHITESPACES
    text = re.sub(r"\s+", " ", text)

    # REMOVE JUNK TEXT
    junk_patterns = [
        r"Back to Top",
        r"back to top",
        r"undefined",
        r"Not Available",
        r"\[at\]",
        r"\[dot\]"
    ]

    for pattern in junk_patterns:
        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE
        )

    return text.strip()