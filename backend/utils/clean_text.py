import re

def clean_text_basic(text: str) -> str:
    text = text.replace("\t", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9.,;:?!()/%\-\n ]", "", text)
    return text.strip()
