import requests
from configs.nettruyenviet_config import HEADERS as NetTruyenUsHeaders

def download_image(image_link, save_path="image.jpg", headers=NetTruyenUsHeaders):
    print(f"Downloading image from {image_link} to {save_path}")
    # Send a GET request to the image URL
    response = requests.get(image_link, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the content of the image
        image_content = response.content

        # Save the image to a file
        with open(save_path, "wb") as file:
            file.write(image_content)
    else:
        print(f"Failed to download image {image_link}. Status code: {response.status_code}")