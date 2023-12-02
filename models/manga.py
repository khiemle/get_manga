class Manga:
    def __init__(self, name, url_link):
        self.name = name
        self.url_link = url_link
        self.chapters = []

    def add_chapter(self, chapter):
        self.chapters.append(chapter)

    def __str__(self) -> str:
        return f'Manga: {self.name}, URL: {self.url_link}, Chapters: {len(self.chapters)}'

