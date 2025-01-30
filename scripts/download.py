import os
import sys
from typing import Dict
import logging
from pathlib import Path

working_directory = Path(__file__).parent.parent
os.chdir(working_directory)
sys.path.append(str(working_directory))

# Import from the current project
from src.data import download
from src import utils

if __name__ == "__main__":
    tv_shows:Dict = utils.read_yaml("configs/config.yaml")["tv-show"]
    os.makedirs("data", exist_ok=True)
    for play_list, url in tv_shows.items():
        download(url, play_list)



