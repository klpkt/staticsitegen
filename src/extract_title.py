def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith("# "):
            return line[2:]
    raise Exception("No title found")