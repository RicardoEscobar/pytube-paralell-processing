"""This generator yields a url for a youtube video by reading it from a given file path."""

def url_generator(path):
    """Yield a url for a youtube video."""
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            yield line.strip()