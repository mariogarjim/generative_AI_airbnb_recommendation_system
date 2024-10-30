import gzip
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from constants import INSIDE_AIRBNB_URL, MADRID_STRING_TO_SCRAP


def inside_airbnb_scrapper():
    """Scrap Madrid airbnb data from "inside airbnb" webpage

    Returns:
        urls(dict): Dictionary with urls to data
    """
    response = requests.get(INSIDE_AIRBNB_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    madrid_section = soup.find("h3", string=MADRID_STRING_TO_SCRAP).find_next("table")

    urls = {}
    for row in madrid_section.find_all("tr"):
        columns = row.find_all("td")
        if len(columns) > 1:
            file_name = columns[1].get_text(strip=True)
            file_url = columns[1].find("a")["href"]
            urls[file_name] = file_url

    return urls

def download_and_uncompress(urls, download_directory="downloads"):
    """Download and uncompress data from URLs into a directory.

    Args:
        urls (dict): Dictionary with URLs to data.
        download_directory (str): Directory to save and uncompress downloaded data.
    """
    create_directory(download_directory)

    for file_name, file_url in urls.items():
        compressed_file_path = Path(download_directory) / file_name
        uncompressed_file_name = (
            file_name.replace(".csv.gz", "_detailed.csv") if file_name.endswith(".gz") else file_name
        )
        uncompressed_file_path = Path(download_directory) / uncompressed_file_name

        if download_file(file_url, compressed_file_path):
            if file_name.endswith(".gz") and uncompress_gz(compressed_file_path, uncompressed_file_path):
                compressed_file_path.unlink()

def create_directory(directory_path):
    """Ensure that a directory exists."""
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def download_file(url, path):
    """Download a file from a URL to a specific path."""
    try:
        response = requests.get(url)
        response.raise_for_status()  
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {path}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return False
    return True


def uncompress_gz(file_path, output_path):
    """Uncompress a .gz file."""
    try:
        with gzip.open(file_path, "rb") as f_in, open(output_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        print(f"Uncompressed {file_path} to {output_path}")
    except (OSError, gzip.BadGzipFile) as e:
        print(f"Failed to uncompress {file_path}: {e}")
        return False
    return True

