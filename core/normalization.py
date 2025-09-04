# core/normalization.py

import unicodedata
import re

def normalize_vietnamese_name(name: str) -> str:
    """
    Normalize Vietnamese names by:
    - Removing excessive whitespace
    - Capitalizing each word (title case)
    """
    if not isinstance(name, str) or not name.strip():
        return ""

    # Remove leading/trailing and normalize internal spaces
    name = re.sub(r'\s+', ' ', name).strip()

    # Standardize known aliases
    replacements = {
        "Uỷ ban nhân dân": "UBND",
        "Ủy ban nhân dân": "UBND",
        "Hội đồng nhân dân": "HĐND",

    }
    for phrase, abbr in replacements.items():
        name = re.sub(rf"\b{re.escape(phrase)}\b", abbr, name, flags=re.IGNORECASE)

    # Title-case each word (preserve Vietnamese diacritics)
    name = name.title()

    return name