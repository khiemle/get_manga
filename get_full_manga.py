import utils.os_utils as OU
import utils.ebook_utils as EU
import utils.network_utils as NU
from configs.nettruyenus_config import HEADERS as NetTruyenUsHeaders
import helpers 
import os
import sys

application_path = os.path.dirname(sys.executable)
print(application_path)
# Get manga URL from the user
url = input("Enter the URL of the manga: ")

# Get manga information
manga = helpers.get_manga(url)

# Print available chapters and indices
print("Available chapters:")
for index, chapter in enumerate(manga.chapters):
    print(f"{index}. {chapter.id} - {chapter.name}")

# Get user input for start and end indices
start_index = int(input("Enter the start index of the chapter: "))
end_index = int(input("Enter the end index of the chapter: "))

# Check indices validity
if not 0 <= start_index < len(manga.chapters) or not 0 <= end_index < len(manga.chapters):
    print("Invalid indices. Exiting.")
    exit()

# ===================
print(f'Manga: {manga.name}')
OU.create_manga_folder(manga)

thumbnail_file_name = "thumbnail.jpg"

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the work_dir path dynamically
work_dir = os.path.join(current_dir, 'workspace', manga.name)

# Create the directory if it doesn't exist
os.makedirs(work_dir, exist_ok=True)

thumbnail = f'{work_dir}/{thumbnail_file_name}'
NU.download_image(manga.thumbnail_url, save_path=thumbnail, headers=NetTruyenUsHeaders)

print(f'Get all pages of each chapter...')
for chapter in manga.chapters[start_index:end_index+1]:
    print(f' Processing {chapter.id}, {chapter.name}, URL: {chapter.url_link}')
    pages = helpers.get_pages_of_chapter(url=chapter.url_link)
    chapter.add_pages(pages)
    print(f' Finished chapter {chapter.id}')

print(f'Download and create pdf...')
for chapter in manga.chapters[start_index:end_index+1]:
    helpers.process_chapter(chapter, work_dir, download_images=True)
    print(f' Downloaded {len(chapter.pages)} images of Chapter {chapter.id}')
    chapter_dir = f'{work_dir}/chapter_{chapter.id}'
    EU.create_pdf_with_images(
        top_left=manga.display_name,
        top_right=chapter.name,
        image_folder=chapter_dir,
        output_path=f'{chapter_dir}.pdf',
        thumbnail_path=thumbnail,
        author=manga.author,
        detail_content=manga.detail_content
    )
    print(f' PDF created at: {chapter_dir}.pdf')
    OU.delete_directory(chapter_dir)
    print(f' Deleted all downloaded images in {chapter_dir} of {chapter.id}')