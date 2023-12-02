from models.page import Page
class Chapter:
    def __init__(self, id, name, url_link):
        self.id = id
        self.name = name
        self.url_link = url_link
        self.pages = []

    def add_page(self, page):
        self.pages.append(page)
    def add_pages(self, pages):
        for page in pages:
            self.pages.append(page)

    def __str__(self) -> str:
        return f'Chapter ID: {self.id}, Chapter: {self.name}, URL: {self.url_link}, Pages: {len(self.pages)}'