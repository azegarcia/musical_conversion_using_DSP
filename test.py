import soundfile as sf
import librosa
import numpy as np

# Load audio without audioread (using soundfile directly)
y, sr = sf.read("piano.wav")  # y is a NumPy array

# If stereo, convert to mono manually
if len(y.shape) == 2:
    y = y.mean(axis=1)

# Use librosa's pyin for pitch detection (no audioread involved)
f0, voiced_flag, voiced_probs = librosa.pyin(
    y,
    fmin=librosa.note_to_hz('A0'),
    fmax=librosa.note_to_hz('C8'),
    sr=sr
)

# Convert detected frequencies to notes
notes = [librosa.hz_to_note(freq) for freq in f0 if freq is not None]
unique_notes = sorted(set(notes))
print("Detected notes:", unique_notes)
