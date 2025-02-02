import yaml
from typing import Dict
import pandas as pd
import numpy as np
import plotly.express as px
from pydub import AudioSegment
import matplotlib.pyplot as plt

def visualize_audio(audio: AudioSegment):
    # Define a function to normalize a chunk to a target amplitude.
    def match_target_amplitude(aChunk, target_dBFS):
        ''' Normalize given audio chunk '''
        change_in_dBFS = target_dBFS - aChunk.dBFS
        return aChunk.apply_gain(change_in_dBFS)
    
    audio = match_target_amplitude(audio, -10)

    # Convert audio to numpy array
    samples = np.array(audio.get_array_of_samples())
    
    # Create a time axis in seconds
    time = np.linspace(0, len(samples) / audio.frame_rate, num=len(samples))
    
    # Plot the waveform using Matplotlib
    plt.figure(figsize=(10, 4))
    plt.plot(time, samples)
    plt.title('Audio Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()

def read_yaml(filename: str) -> Dict:
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

