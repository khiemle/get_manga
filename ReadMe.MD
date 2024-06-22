
## Install required python package
```
pip install -r requirements.txt
```
Lock the version of those packages:
```
pip freeze > requirements.txt
```

## Notes

If got message "error: externally-managed-environment". Run those command
```
python3 -m venv path/to/venv
source path/to/venv/bin/activate
python3 -m pip install pytube
```

## Get Chrome WebDriver 

https://getwebdriver.com/chromedriver#stable

Download and extract to a folder and add the Path of this folder to $PATH
Open Settings --> Privacy and Security --> Allow chromedriver 


## Download Manga

- Open https://nettruyenviet.com/ and get the manga url. Example: https://nettruyenviet.com/truyen-tranh/tuyen-tap-chiba-tetsuya-gaki
- Run the command format `python3` `get_full_manga.py` `<manga_url>` `<start_chapter_index>` `<end_chapter_index>`

```
python3 get_full_manga.py https://nettruyenviet.com/truyen-tranh/tuyen-tap-chiba-tetsuya-gaki 0 1 ~/Workspace/manga
```