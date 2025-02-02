# code inspired from from https://stackoverflow.com/questions/45526996/split-audio-files-using-silence-detection

import os
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tqdm import tqdm

class SilenceAudioSplitter:
    def __init__(self, min_silence_len:int = 2000, silence_thresh:int = -210, normalization_dBFS = -20):
        self.min_silence_len = min_silence_len
        self.silence_thresh = silence_thresh
        self.normalization_dBFS = normalization_dBFS
    
    # Define a function to normalize a chunk to a target amplitude.
    def match_target_amplitude(self, aChunk, target_dBFS):
        ''' Normalize given audio chunk '''
        change_in_dBFS = target_dBFS - aChunk.dBFS
        return aChunk.apply_gain(change_in_dBFS)
    
    def split_on_silence_and_save(self, audio_path:str, audio_name:str, save_path:Path):
        os.makedirs(save_path, exist_ok=True)

        # Load your audio.
        if str(audio_path).endswith('.mp3'):
            audio = AudioSegment.from_mp3(audio_path)
        elif str(audio_path).endswith('.wav'):
            audio = AudioSegment.from_wav(audio_path)

        audio = self.match_target_amplitude(audio, self.normalization_dBFS)

        chunks = split_on_silence (
            # Use the loaded audio.
            audio, 
            # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
            min_silence_len = self.min_silence_len,
            # Consider a chunk silent if it's quieter than -16 dBFS.
            silence_thresh = self.silence_thresh
        )
        
        # A list to store the audio chunks
        chunk_lists = []

        # Process each chunk with your parameters
        i = 0
        for chunk in tqdm(chunks):
            # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
            silence_chunk = AudioSegment.silent(duration=500)

            # Add the padding chunk to beginning and end of the entire chunk.
            audio_chunk = silence_chunk + chunk + silence_chunk

            # Keep only the audios longer than 1,5 seconds (we assumes that saying a word should take longer)
            # Mind reconsidering it and adjust it
            if len(audio_chunk) > 1500:
                # Normalize the entire chunk.
                normalized_chunk = self.match_target_amplitude(audio_chunk, -20.0)

                # Export the audio chunk with new bitrate.
                # print(f"Exporting {audio_name}_chunk_{i}.mp3")
                normalized_chunk.export(
                    os.path.join(save_path, f"{audio_name}_chunk_{i}.mp3"),
                    bitrate = "192k",
                    format = "mp3"
                )

                chunk_lists.append(f"{audio_name}_chunk_{i}.mp3")

                i += 1

        return chunk_lists