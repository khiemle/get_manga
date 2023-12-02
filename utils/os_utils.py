import os
import shutil
def create_manga_folder(manga):
    # Define the path to the workspace directory
    workspace_path = os.path.join(".", "workspace")

    # Create a folder for the Manga object
    manga_folder_path = os.path.join(workspace_path, manga.name)

    # Check if the folder already exists, if not, create it
    if not os.path.exists(manga_folder_path):
        os.makedirs(manga_folder_path)
        print(f'Folder created for {manga.name}: {manga_folder_path}')
    else:
        print(f'Folder already exists for {manga.name}: {manga_folder_path}')


def delete_directory(directory):
    try:
        shutil.rmtree(directory)
        print(f'Deleted directory: {directory}')
    except OSError as e:
        print(f'Error deleting directory {directory}: {e}')