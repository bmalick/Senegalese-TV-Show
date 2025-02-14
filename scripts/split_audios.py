import os
import sys
from pathlib import Path
import logging

working_directory = Path(__file__).parent.parent
os.chdir(working_directory)
sys.path.append(str(working_directory))

from src.data.silence_audio_splitter import SilenceAudioSplitter
from src.data.custom_silence_audio_splitter import split_audio_on_silence
AUDIO_PATH = Path(r"data\promesses\Interview  - Promesses - Saison 1 - ＂PARLONS D'AMOUR＂ - VOSTFR.mp3")

def main():
    split_audio_on_silence(AUDIO_PATH, min_silence_len=4, silence_thresh=-3, hop_length=256, frame_length=512)



if __name__ == "__main__":
    main()