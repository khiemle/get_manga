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
import utils.os_utils as OU
import utils.ebook_utils as EU
import utils.network_utils as NU
import utils.common_utils as CU

def get_pages_of_chapter(url):
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
    for container in containers:
        src = container.find_element(by="xpath", value="./img").get_attribute("src")
        number = container.get_attribute("id")
        pageList.append(Page(src, number))

    # Quit the WebDriver
    driver.quit()

    return pageList

def get_manga(url):
    options = Options()
    options.headless = False
    # Create a Chrome WebDriver instance
    driver = webdriver.Chrome(options=options)

    # Open the URL
    driver.get(url)

    # Wait for the elements to be present
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-xs-5 chapter']")))


    # Find elements with the specified XPath
    containers = driver.find_elements(by="xpath", value="//div[@class='col-xs-5 chapter']")

    # Extract href values
    # href_list = [container.find_element(by="xpath", value="./a").get_attribute("href") for container in containers]

    # Create a Manga object
    manga = Manga(name=CU.get_manga_name_from_url(url), url_link=url)

    # Extract and add Chapter objects to the Manga
    for container in containers:
        chapter_name = container.find_element(by="xpath", value="./a").text
        chapter_url = container.find_element(by="xpath", value="./a").get_attribute("href")
        chapter = Chapter(id=CU.get_chapter_id_from_url(chapter_url),name=chapter_name, url_link=chapter_url)
        manga.add_chapter(chapter)

    # Quit the WebDriver
    driver.quit()

    return manga

def process_chapter(chapter, work_dir, download_images=True):
    chapter_dir = os.path.join(work_dir, f"chapter_{chapter.id}")
    os.makedirs(chapter_dir, exist_ok=True)

    print(f'Downloading Chapter {chapter.id}, {chapter.name}, URL: {chapter.url_link}')

    for page in chapter.pages:
        image_url = page.src
        image_filename = f'{page.number}.jpg'
        image_path = os.path.join(chapter_dir, image_filename)

        if download_images:
            NU.download_image(image_url, image_path)
            print(f'  Downloaded page {page.number}: {image_filename}')
        else:
            print(f'  Image URL for page {page.number}: {image_url}')

# ===================
url = "https://www.nettruyenus.com/truyen-tranh/doc-thoai-cua-nguoi-duoc-si-178400"
manga = get_manga(url)

print(f'Manga: {manga.name}')
OU.create_manga_folder(manga)

work_dir = f'/Users/khle/Workspace/Projects/py_auto/workspace/{manga.name}'
for chapter in manga.chapters:
    print(f' Processing {chapter.id}, {chapter.name}, URL: {chapter.url_link}')
    pages = get_pages_of_chapter(url=chapter.url_link)
    chapter.add_pages(pages)

for chapter in manga.chapters:
    print(f'start chapter {chapter.id}')
    list_image_urls = []
    for page in chapter.pages:
        list_image_urls.append(page.src)

    process_chapter(chapter, work_dir, download_images=True)

    chapter_dir = f'{work_dir}/chapter_{chapter.id}'

    EU.create_pdf_with_images(
        title=chapter.id,
        author="Khiem Le",
        image_folder=chapter_dir,
        output_path=f'{chapter_dir}.pdf'
    )
    OU.delete_directory(chapter_dir)
    print(f'finished chapter {chapter.id}')

