import yt_dlp
import yaml
import os

# Function to read URLs from a YAML file
def read_urls_from_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

# Function to rename the downloaded files
def rename_file(old_name):
    directory, filename = os.path.split(old_name)
    name, ext = os.path.splitext(filename)
    new_name = f"{name.lower().replace(' ', '-')}{ext}"
    new_path = os.path.join(directory, new_name)
    os.rename(old_name, new_path)
    print(f"Renamed {old_name} to {new_path}")

# Function to log the URL of successfully downloaded videos
def log_downloaded_url(log_file, url):
    with open(log_file, 'a') as file:
        file.write(url + '\n')

# Function to check if a URL has already been downloaded
def is_url_downloaded(log_file, url):
    if not os.path.exists(log_file):
        return False
    with open(log_file, 'r') as file:
        downloaded_urls = file.read().splitlines()
    return url in downloaded_urls

# Function to download a single video
def download_video(url, category, ydl_opts, log_file):
    while True:
        try:
            if is_url_downloaded(log_file, url):
                print(f"Skipping already downloaded video: {url}")
                return
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                old_name = ydl.prepare_filename(info_dict)
                rename_file(old_name)
                log_downloaded_url(log_file, url)
                print(f"Successfully downloaded and renamed: {url}")
            break
        except Exception as e:
            print(f"Failed to download {url}: {e}. Retrying...")

# Function to download videos sequentially
def download_videos(urls, category):
    ydl_opts = {
        'format': 'bestvideo[height<=480]+bestaudio/best',  # 480p and lower quality
        'outtmpl': f'downloads/{category}/%(title)s.%(ext)s',  # Save files in the 'downloads/category' folder
    }
    
    os.makedirs(f'downloads/{category}', exist_ok=True)  # Create the folder if it doesn't exist

    log_file = f'downloads/{category}_downloaded.log'

    for url in urls:
        download_video(url, category, ydl_opts, log_file)

# Main code
video_data = read_urls_from_yaml('video_urls.yaml')

for category, urls in video_data.items():
    print(f"Downloading videos for category: {category}")
    download_videos(urls, category)
