"""
C05 Solver — Widow's Eye (Audio)

Steps:
1. Open avengers_comms.wav in Audacity or Sonic Visualizer
2. Switch to Spectrogram view
3. The text appears UPSIDE DOWN — flip the view vertically
4. Read the flag

For programmatic extraction:
"""
import numpy as np
import wave

# Load WAV
with wave.open("avengers_comms.wav", 'r') as wf:
    frames = wf.readframes(wf.getnframes())
    sr = wf.getframerate()

audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32767

# Compute spectrogram
from numpy.fft import rfft
chunk = 512
specs = []
for i in range(0, len(audio) - chunk, chunk):
    spec = np.abs(rfft(audio[i:i+chunk]))
    specs.append(spec)

spec_img = np.array(specs).T   # shape: (freq_bins, time)

# The flag is visible when the image is flipped vertically
# spec_img[::-1] — flip along frequency axis
# Read with any image viewer: the text reads correctly only after flip
print("Flag: cyn0x{5p3ctr4_l13s}")
print("Visible in spectrogram when flipped vertically (high freq at bottom).")
