class Page:
    def __init__(self, src, number):
        self.src = src
        self.number = number
    def __str__(self) -> str:
        return f'@{self.src} - @{self.number}'