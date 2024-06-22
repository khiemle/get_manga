class Manga:
    def __init__(self, name, url_link, author=None, display_name=None, thumbnail_url=None, status=None, detail_content=None):
        self.name = name
        self.url_link = url_link
        self.author = author
        self.display_name = display_name
        self.thumbnail_url = thumbnail_url
        self.status = status
        self.chapters = []
        self.detail_content = detail_content

    def add_chapter(self, chapter):
        self.chapters.append(chapter)
    
    def print_manga_details(self):
        print(f'{ "Full Name:".ljust(15) } {self.display_name}')
        print(f'{ "Author:".ljust(15) } {self.author}')
        print(f'{ "Status:".ljust(15) } {self.status}')
        print(f'{ "Chapters:".ljust(15) } {len(self.chapters)}')
        print(f'{ "Detail content:".ljust(15) } {self.detail_content}')

    def __str__(self) -> str:
        return f'Manga: {self.name}, URL: {self.url_link}, Author: {self.author}, Display Name: {self.display_name}, ' \
               f'Thumbnail URL: {self.thumbnail_url}, Status: {self.status}, Chapters: {len(self.chapters)}'



