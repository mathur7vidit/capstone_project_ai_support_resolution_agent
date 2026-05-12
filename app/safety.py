import re

unsafe_keywords = [
    "hack",
    "bypass",
    "steal"
]

sensitive_keywords = [
    "lawsuit",
    "legal",
    "fraud",
    "payment dispute"
]


def mask_pii(text: str):
    return re.sub(r'\d', '*', text)


def is_unsafe(text: str):
    text = text.lower()

    for word in unsafe_keywords:
        if word in text:
            return True

    return False


def requires_escalation(text: str):
    text = text.lower()

    for word in sensitive_keywords:
        if word in text:
            return True

    return False