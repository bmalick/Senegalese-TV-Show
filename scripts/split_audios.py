import os
import sys
from pathlib import Path
from pydub import AudioSegment
import logging

working_directory = Path(__file__).parent.parent
os.chdir(working_directory)
sys.path.append(str(working_directory))

from src.data.silence_audio_splitter import SilenceAudioSplitter
from src.utils import visualize_audio
AUDIO_PATH = Path("data\promesses\Interview  - Promesses - Saison 1 - ＂PARLONS D'AMOUR＂ - VOSTFR.mp3")

def main():
    # # Visualize the audio first to adapt the different parameters of the splitting
    # # Load your audio.
    # if str(AUDIO_PATH).endswith('.mp3'):
    #     audio = AudioSegment.from_mp3(AUDIO_PATH)
    # elif str(AUDIO_PATH).endswith('.wav'):
    #     audio = AudioSegment.from_wav(AUDIO_PATH)

    # visualize_audio(audio)

    silenceAudioSplitter = SilenceAudioSplitter(min_silence_len = 5, silence_thresh = -30, normalization_dBFS = -10)
    _ = silenceAudioSplitter.split_on_silence_and_save(AUDIO_PATH, "test", Path("data/test"))


if __name__ == "__main__":
    main()