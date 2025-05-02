import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq
import scipy.io.wavfile as wav
import json
from music21 import stream, note, chord, midi, converter, environment
import matplotlib.pyplot as plt
import sys

NOTES_MAP = json.load(open("notes_map.json", "r"))

WAVE_LOCATION = "piano.wav"
DURATION = 300  # should be in seconds # 5 mins 7 secs
wav_file = open(WAVE_LOCATION, "rb")
SAMPLE_RATE, data = wav.read(wav_file)

# Plot the time domain
t = 1 * np.arange(SAMPLE_RATE*DURATION)
plt.plot(t, data[:SAMPLE_RATE*DURATION])
# magnitude graph
plt.savefig('magnitude.png')

yf = fft(data[:SAMPLE_RATE*DURATION])
xf = fftfreq(SAMPLE_RATE*DURATION, 1 / SAMPLE_RATE)
plt.plot(xf, np.abs(yf))
plt.xlim([0, 3e3])
# plt.xlim([0, 1e7])
plt.savefig('frequency.png')

# Map frequencies to magnitude
y = np.abs(yf)

d = {}
for i in range(0, len(y)):
  if xf[i] > 0:
    d[f"{xf[i]}"] = y[i]

# Sort the dict so highest frequencies are at the top
d = sorted(d, reverse=True)

# Get the top 10 notes
bucket = []
for i in d:
  i = round(float(i))
  if i not in bucket:
    bucket.append(i)

# Map to notes
notes = []
for i in bucket:
  for note in NOTES_MAP:
    note_freq = NOTES_MAP[note]

    l_r = i - 4
    h_r = i + 4
    if l_r < note_freq and h_r > note_freq:
      notes.append(note)
      break

processed_notes = list(set(notes))
lilypond_content = r'''
\version "2.24.2"
\relative c' {
  \clef treble
  \key c \major
  \time 4/4
  % Notes will be inserted here
'''

# Add the notes
lilypond_content += '  ' + ' '.join(processed_notes) + '\n}\n'

# Save to file
with open('generated_music.ly', 'w') as f:
    f.write(lilypond_content)
      