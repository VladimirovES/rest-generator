import re

def remove_underscores(name: str) -> str:
    segments = name.split('_')
    cleaned_segments = []
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        if re.match(r'^[A-Z][a-zA-Z0-9]*$', seg):
            cleaned_segments.append(seg)
        else:
            cleaned_segments.append(seg.capitalize())
    return ''.join(cleaned_segments)

def class_name_from_tag(tag: str) -> str:
    """Простая логика: заменяем '-' -> '_', split и склеиваем в CamelCase."""
    tag = tag.replace('-', '_')
    parts = re.split(r'[\s_]+', tag)
    return ''.join(word.capitalize() for word in parts if word)
