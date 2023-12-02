import pdfkit
import os

# Configure pdfkit options (equivalent to Kotlin settings)
options = {
    'orientation': 'Portrait',
    'page-size': 'A5',
    'margin-top': '0in',
    'margin-bottom': '0in',
    'margin-left': '0in',
    'margin-right': '0in',
    'enable-local-file-access': ''
}

# Define a function to create a PDF
def create_pdf_by_lib(lst_images, pdf_name):
    print(f"Wrapping image urls and creating {pdf_name} file ...")

    # Create HTML content with image tags
    image_tags = [f'<img style="width:100%; max-height:960px;" src="{image_url}" /><br/>' for image_url in lst_images]
    html_content = '<html><head><meta charset="utf-8"></head><body>{}</body></html>'.format("".join(image_tags))

    # Generate PDF from HTML content
    pdfkit.from_string(html_content, pdf_name, options=options)

    print("Done")

def create_pdf_with_images(top_left, top_right, image_folder, output_path, thumbnail_path=None, author=None, detail_content=None):
    # Create a new HTML string with images
    html_content = generate_html_with_images_v2(manga_name=top_left, chapter_name=top_right, image_folder=image_folder, thumbnail_path=thumbnail_path, author=author, detail_content=detail_content)

    # Generate PDF from HTML content
    pdfkit.from_string(html_content, output_path, options=options)

    print(f'PDF created at: {output_path}')

def extract_number_from_filename(filename):
    # Assuming the filename format is "page_<number>.jpg"
    prefix, number = filename.split("_", 1)
    number, _ = os.path.splitext(number)
    return int(number)

def generate_html_with_images(image_folder):
    # Get a list of image files in the specified folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Sort image_files based on the numeric part of the filename
    sorted_image_files = sorted(image_files, key=extract_number_from_filename)


     # Generate HTML with each image wrapped in a <div>
    image_tags = [f'<div><img style="width:100%; max-height:960px;" src="file://{image_folder}/{image_file}" alt="Image {index + 1}"/></div>' for index, image_file in enumerate(sorted_image_files)]
    html_content = f'<html><head><meta charset="utf-8"></head><body>{"".join(image_tags)}</body></html>'

    return html_content

def generate_html_with_images_v2(manga_name, chapter_name, image_folder, thumbnail_path=None, author = None, detail_content=None):
    # Get a list of image files in the specified folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Sort image_files based on the numeric part of the filename
    sorted_image_files = sorted(image_files, key=extract_number_from_filename)

    thumbnail_tag = f'<img style="min-height: 200px; max-height: 250px;" src="{thumbnail_path}" alt="Thumbnail">' if thumbnail_path else ''

    author_tag = f'  <div style="font-size: 14px; font-weight: bold;">{author}</div>' if author else ''

    intro_tag = f'<div style="width: 100%; height: 960px; position: relative; text-align: center; font-family: \'Arial\', Helvetica, sans-serif;">' \
                f'  <div style="width: 100%; height: 250px;"></div>' \
                f'  {thumbnail_tag}' \
                f'  <div style="width: 100%; height: 20px;"></div>' \
                f'  <div style="font-size: 14px; font-weight: bold;">{manga_name}</div>' \
                f'  {author_tag}' \
                f'  <div style="width: 100%; height: 20px;"></div>' \
                f'  <div style="width: 80%; font-size: 14px; font-weight: bold; margin: 0 auto; display: flex; align-items: center;">{detail_content}</div>' \
                f'  <div style="width: 100%; height: 20px;"></div>' \
                f'  <div style="font-size: 14px; font-weight: bold;">{chapter_name}</div>' \
                f'  <div style="width: 100%; height: 20px;"></div>' \
                f'  <div style="font-size: 14px; font-weight: bold;">Pdf created by JQKA</div>' \
                f'</div>'

    # Generate HTML with each image wrapped in a <div> and additional elements
    image_tags = [f'<div><img style="width:100%; max-height:960px;" src="file://{image_folder}/{image_file}" alt="Image {index + 1}"/></div>' for index, image_file in enumerate(sorted_image_files)]
    html_content = f'<html><head><meta charset="utf-8"></head><body>{intro_tag}{"".join(image_tags)}</body></html>'

    return html_content
