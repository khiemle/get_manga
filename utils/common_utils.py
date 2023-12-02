import re
from urllib.parse import urlparse

def get_manga_name_from_url(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Split the path and get the last part (Manga name)
    manga_name = parsed_url.path.split("/")[-1]

    return manga_name
def get_chapter_id_from_url(url):
    # Define a regular expression pattern to match the chapter id
    pattern = re.compile(r'/chap-([^/]+)/')

    # Search for the pattern in the URL
    match = pattern.search(url)

    if match:
        # Extract and return the chapter id
        chapter_id = match.group(1)
        return chapter_id
    else:
        # Return None if no match is found
        return None