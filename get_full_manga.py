import utils.os_utils as OU
import utils.ebook_utils as EU
import helpers 

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
if not 1 <= start_index <= len(manga.chapters) or not 1 <= end_index <= len(manga.chapters):
    print("Invalid indices. Exiting.")
    exit()

# ===================

# ===================
# url = "https://www.nettruyenus.com/truyen-tranh/doc-thoai-cua-nguoi-duoc-si-178400"
# manga = helpers.get_manga(url)

print(f'Manga: {manga.name}')
OU.create_manga_folder(manga)

work_dir = f'/Users/khle/Workspace/Projects/py_auto/workspace/{manga.name}'
for chapter in manga.chapters[start_index-1:end_index]:
    print(f' Processing {chapter.id}, {chapter.name}, URL: {chapter.url_link}')
    pages = helpers.get_pages_of_chapter(url=chapter.url_link)
    chapter.add_pages(pages)

for chapter in manga.chapters[start_index-1:end_index]:
    print(f'start chapter {chapter.id}')
    helpers.process_chapter(chapter, work_dir, download_images=True)
    chapter_dir = f'{work_dir}/chapter_{chapter.id}'
    EU.create_pdf_with_images(
        title=chapter.id,
        author="Khiem Le",
        image_folder=chapter_dir,
        output_path=f'{chapter_dir}.pdf'
    )
    OU.delete_directory(chapter_dir)
    print(f'finished chapter {chapter.id}')