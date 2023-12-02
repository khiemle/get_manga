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

def get_pages_of_chapter(url) -> List[Page]:
    options = Options()
    options.headless = False
    # Create a Chrome WebDriver instance
    driver = webdriver.Chrome(options=options)

    # Open the URL
    driver.get(url)

    # Wait for the elements to be present
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='page-chapter']")))


    # Find elements with the specified XPath
    containers = driver.find_elements(by="xpath", value="//div[@class='page-chapter']")

    pageList = []
    for index,container in enumerate(containers):
        src = container.find_element(by="xpath", value="./img").get_attribute("src")
        number = f'page_{index}'
        pageList.append(Page(src, number))

    # Quit the WebDriver
    driver.quit()

    return pageList

def get_manga(url) -> Manga:
    options = Options()
    options.headless = False
    # Create a Chrome WebDriver instance
    driver = webdriver.Chrome(options=options)

    # Open the URL
    driver.get(url)

    # Wait for the elements to be present
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-xs-5 chapter']")))

    author = SU.get_text_by_xpath(driver=driver, xpath="//li[@class='author row']//a")
    status = SU.get_text_by_xpath(driver=driver, xpath="//li[@class='status row']//p[@class='col-xs-8']")
    display_name = SU.get_text_by_xpath(driver=driver, xpath="//h1[@class='title-detail']")
    thumbnail_url = SU.get_attribute_by_xpath(driver=driver, xpath="//div[@class='col-xs-4 col-image']//img", attribute="src")
    detail_content = SU.get_text_by_xpath(driver=driver, xpath="//div[@class='detail-content']//p")

    # Find elements with the specified XPath
    containers = driver.find_elements(by="xpath", value="//div[@class='col-xs-5 chapter']")

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

    manga.print_manga_details()

    # Quit the WebDriver
    driver.quit()

    return manga

def process_chapter(chapter, work_dir, download_images=True):
    chapter_dir = os.path.join(work_dir, f"chapter_{chapter.id}")
    os.makedirs(chapter_dir, exist_ok=True)

    for page in chapter.pages:
        image_url = page.src
        image_filename = f'{page.number}.jpg'
        image_path = os.path.join(chapter_dir, image_filename)

        if download_images:
            NU.download_image(image_url, image_path)
        else:
            print(f'  Image URL for page {page.number}: {image_url}')


