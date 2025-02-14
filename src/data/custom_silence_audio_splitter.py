import numpy as np
import pydub 
from pathlib import Path
import os
from tqdm import tqdm
import json


""" The read and write function are obtained fro https://stackoverflow.com/questions/53633177/how-to-read-a-mp3-audio-file-into-a-numpy-array-save-a-numpy-array-to-mp3 """

def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y

def write(f, sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    song.export(f, format="mp3", bitrate="320k")


def get_averaged_audio_if_two_channels(audio:np.array):
    if audio.ndim == 2 and audio.shape[1] == 2:
        return np.mean(audio, axis=1)
    return audio

def get_audio_energy_array(audio:np.array, hop_length:int = 256, frame_length:int = 512):
    audio_length = len(audio)
    return np.array([
        sum(audio[i:i+frame_length]**2)
        for i in range(0, audio_length, hop_length)
    ])


def get_log_scaled_energy_audio(audio_energy:np.array):
    max_energy = np.max(audio_energy)
    min_energy = np.min(audio_energy)
    scaled_energy = (audio_energy - min_energy) / (max_energy - min_energy)
    scaled_energy = scaled_energy *1000  # Scale to range [1, 10]
    return np.log(scaled_energy)

def split_audio_on_silence(
        audio_path:Path,
        min_silence_len:int = 2000, 
        silence_thresh:int = -210,
        hop_length:int = 256,
        frame_length:int = 512,
    ):

    sr, audio_2_channels = read(audio_path)
    audio = get_averaged_audio_if_two_channels(audio_2_channels)
    audio_energy = get_audio_energy_array(audio, hop_length=hop_length, frame_length=frame_length)
    log_scaled_energy = get_log_scaled_energy_audio(audio_energy)

    split_frame_index = [0]
    silent_length = 0
    print(log_scaled_energy)
    log_scaled_energy_dict = {i: log_scaled_energy[i] for i in range(len(log_scaled_energy))}
    # with open('energy.json', 'w') as file:
    #     json.dump(log_scaled_energy_dict, file, indent=4)
    
    for i, scaled_frame_energy in tqdm(enumerate(log_scaled_energy)):
        if scaled_frame_energy <= silence_thresh:
            silent_length += 1
        else:
            if silent_length >= min_silence_len:
                new_index = int(i - silent_length/2)
                if new_index - split_frame_index[-1] >= 100:
                    split_frame_index.append(new_index)
            silent_length = 0
    split_frame_index.append(len(log_scaled_energy))
    print(len(split_frame_index))

    split_audios_array = [audio[split_frame_index[i]*frame_length:split_frame_index[i+1]*frame_length] for i in range(len(split_frame_index) - 1)]
    os.makedirs(r'data\\test_custom', exist_ok=True)
    for i, split in enumerate(split_audios_array):
        write(os.path.join(r'data\\test_custom', f'audio_{i}.mp3'), sr, split)
