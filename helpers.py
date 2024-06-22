from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from models.page import Page
from models.chapter import Chapter
from models.manga import Manga
import os
import utils.network_utils as NU
import utils.common_utils as CU
import utils.selenium_utils as SU
from typing import List
from configs.source_configs import source_configs

def get_pages_of_chapter(url) -> List[Page]:
    source_config = None
    for config in source_configs:
        if url.startswith(config.main_page_url):
            source_config = config
            break

    if not source_config:
        raise ValueError("URL does not match any source configuration.")
    
    options = Options()
    options.headless = True
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    # Create a Chrome WebDriver instance
    driver = webdriver.Chrome(options=options)

    # Open the URL
    driver.get(url)

    # Wait for the elements to be present
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, source_config.pages_container_xpath)))


    # Find elements with the specified XPath
    imgs = driver.find_elements(by="xpath", value=source_config.pages_container_xpath)

    pageList = []
    for index,img_element in enumerate(imgs):
        srcs = [img_element.get_attribute(attr) for attr in source_config.img_src_list]
        src = next((src for src in srcs if src is not None), None)
        number = f'page_{index}'
        pageList.append(Page(src, number))

    # Quit the WebDriver
    driver.quit()

    return pageList

def get_manga(url) -> Manga:
    source_config = None
    for config in source_configs:
        if url.startswith(config.main_page_url):
            source_config = config
            break

    if not source_config:
        raise ValueError("URL does not match any source configuration.")
    options = Options()
    options.headless = True
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    # Create a Chrome WebDriver instance
    driver = webdriver.Chrome(options=options)

    # Open the URL
    driver.get(url)

    # Wait for the elements to be present
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, source_config.chapters_container_xpath)))

    author = SU.get_text_by_xpath(driver=driver, xpath=source_config.author_xpath)
    status = SU.get_text_by_xpath(driver=driver, xpath=source_config.status_xpath)
    display_name = SU.get_text_by_xpath(driver=driver, xpath=source_config.display_name_xpath)
    thumbnail_url = SU.get_attribute_by_xpath(driver=driver, xpath=source_config.thumbnail_url_img_xpath, attribute="src")
    detail_content = SU.get_text_by_xpath(driver=driver, xpath=source_config.detail_content_xpath)

    # Find elements with the specified XPath
    containers = driver.find_elements(by="xpath", value=source_config.chapters_container_xpath)

    # Extract href values
    # href_list = [container.find_element(by="xpath", value="./a").get_attribute("href") for container in containers]

    # Create a Manga object
    manga = Manga(name=CU.get_manga_name_from_url(url), 
                  url_link=url, 
                  author=author, 
                  status=status, 
                  display_name=display_name, 
                  thumbnail_url=thumbnail_url,
                  detail_content=detail_content)

    # Extract and add Chapter objects to the Manga
    for container in containers:
        chapter_name = container.find_element(by="xpath", value="./a").text
        chapter_url = container.find_element(by="xpath", value="./a").get_attribute("href")
        chapter = Chapter(id=CU.get_chapter_id_from_url(chapter_url),name=chapter_name, url_link=chapter_url)
        manga.add_chapter(chapter)
    manga.chapters.reverse()

    manga.print_manga_details()

    # Quit the WebDriver
    driver.quit()

    return manga

def process_chapter(chapter, work_dir, download_images=True):
    chapter_dir = os.path.join(work_dir, f"{chapter.id}")
    os.makedirs(chapter_dir, exist_ok=True)

    for page in chapter.pages:
        image_url = page.src
        image_filename = f'{page.number}.jpg'
        image_path = os.path.join(chapter_dir, image_filename)

        if download_images and image_url is not None:
            NU.download_image(image_url, image_path)
        else:
            print(f'  Image URL for page {page.number}: {image_url}')


