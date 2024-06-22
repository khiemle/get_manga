import re
from urllib.parse import urlparse

def get_manga_name_from_url(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Split the path and get the last part (Manga name)
    manga_name = parsed_url.path.split("/")[-1]

    return manga_name
def get_chapter_id_from_url(url):
    # Split the URL by '/'
    parts = url.split('/')
    
    # Get the last non-empty part of the split URL
    # This handles cases where the URL might end with a '/'
    chapter_id = next((part for part in reversed(parts) if part), None)
    
    return chapter_id