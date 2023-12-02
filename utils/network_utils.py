import requests
from configs.nettruyenus_config import HEADERS as NetTruyenUsHeaders

def download_image(image_link, save_path="image.jpg", headers=NetTruyenUsHeaders):
    # Send a GET request to the image URL
    response = requests.get(image_link, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the content of the image
        image_content = response.content

        # Save the image to a file
        with open(save_path, "wb") as file:
            file.write(image_content)
            print(f"Image downloaded successfully and saved as {save_path}.")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")