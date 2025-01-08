def extract_between_markers(text: str, start_tag: str, end_tag: str) -> str:
    start = text.find(start_tag) + len(start_tag)
    end = start + text[start:].find(end_tag)
    return text[start:end].strip()
