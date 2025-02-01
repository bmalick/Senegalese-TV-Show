import os
import sys
from pathlib import Path
import logging

working_directory = Path(__file__).parent.parent
os.chdir(working_directory)
sys.path.append(str(working_directory))

from src.data.silence_audio_splitter import SilenceAudioSplitter
AUDIO_PATH = Path("data\promesses\Interview  - Promesses - Saison 1 - ＂PARLONS D'AMOUR＂ - VOSTFR.mp3")

def main():
    silenceAudioSplitter = SilenceAudioSplitter(min_silence_len = 5, silence_thresh = -70)
    _ = silenceAudioSplitter.split_on_silence_and_save(AUDIO_PATH, "test", Path("data/test"))


if __name__ == "__main__":
    main()