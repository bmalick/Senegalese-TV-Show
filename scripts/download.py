import os
import logging

from src.data import download
from src import utils


if __name__ == "__main__":
    tv_shows = utils.read_yaml("configs/config.yaml")["tv-show"]
    os.makedirs("data", exist_ok=True)
    for name, url in tv_shows.items():
        print(url)
        download.download_playlist(name, url, "audio")
