import configparser

class SourceConfig:
    def __init__(self, ini_file):
        self.config = configparser.ConfigParser()
        self.config.read(ini_file)
        
        # Main Page
        self.main_page_url = self.config.get('main_page', 'url')
        
        # Manga Page
        self.author_xpath = self.config.get('manga_page', 'author_xpath')
        self.status_xpath = self.config.get('manga_page', 'status_xpath')
        self.display_name_xpath = self.config.get('manga_page', 'diplay_name_xpath')  # Note the typo in 'diplay'
        self.thumbnail_url_img_xpath = self.config.get('manga_page', 'thumbnail_url_img_xpath')
        self.detail_content_xpath = self.config.get('manga_page', 'detail_content_xpath')
        self.chapters_container_xpath = self.config.get('manga_page', 'chapters_container_xpath')
        
        # Chapter Page
        self.pages_container_xpath = self.config.get('chapter_page', 'pages_container_xpath')
        self.img_src_list = self.config.get('chapter_page', 'img_src_list').split(',')

# Example usage
net_truyen_viet_config = SourceConfig('configs/nettruyenviet.ini')
blogtruyen_config = SourceConfig('configs/blogtruyen.ini')
source_configs = [net_truyen_viet_config, blogtruyen_config]