import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq
import scipy.io.wavfile as wav
import json
from music21 import *
import matplotlib.pyplot as plt
import time
import subprocess

def identify_instrument():
  if instrument == "Bass":
    notes_map = "bass_map.json"
  elif instrument == "Flute":
    notes_map = "flute_map.json"
  elif instrument == "Piano":
    notes_map = "notes_map.json"
  elif instrument == "Saxophone":
    notes_map = "saxo_map.json"
  else:
    notes_map = "violin_map.json"
  
  return notes_map

def pitch_to_lilypond(note):
    base_map = {'C': 'c', 'D': 'd', 'E': 'e', 'F': 'f', 'G': 'g', 'A': 'a', 'B': 'b'}
    accidental_map = {'#': 'is', 'b': 'es'}
    
    # Split pitch and octave
    if len(note) == 2:
        pitch, octave = note[0], int(note[1])
        accidental = ''
    else:
        pitch, accidental, octave = note[0], note[1], int(note[2])
        accidental = accidental_map.get(accidental, '')

    lily_note = base_map[pitch] + accidental
    
    # Determine octave offset (C4 = c')
    offset = octave - 3
    if offset > 0:
        lily_note += "'" * offset
    elif offset < 0:
        lily_note += "," * abs(offset)
    
    return lily_note + "4"  # quarter note
  
notes_map = identify_instrument()
NOTES_MAP = json.load(open(notes_map, "r"))
environment.UserSettings()['lilypondPath'] =  'C:/Lilypond/usr/bin/lilypond.exe'
start = time.time()

WAVE_LOCATION = "piano.wav"
DURATION = 270  # should be in seconds # 5 mins 7 secs
wav_file = open(WAVE_LOCATION, "rb")
SAMPLE_RATE, data = wav.read(wav_file)

# Plot the time domain
t = 1 * np.arange(SAMPLE_RATE*DURATION)
plt.plot(t, data[:SAMPLE_RATE*DURATION])

# magnitude graph
print("Plotting magnitudes..")
plt.savefig('magnitude.png')

yf = fft(data[:SAMPLE_RATE*DURATION])
xf = fftfreq(SAMPLE_RATE*DURATION, 1 / SAMPLE_RATE)
plt.plot(xf, np.abs(yf))
plt.xlim([0, 3e3])
print("Plotting frequencies..")
plt.savefig('frequency.png')

# Map frequencies to magnitude
y = np.abs(yf)
d = {}
for i in range(0, len(y)):
  if xf[i] > 0:
    d[f"{xf[i]}"] = y[i]

# Sort the dict so highest frequencies are at the top
print("Sorting to get the high frequencies..")
d = sorted(d, reverse=True)

# Get the top notes
bucket = []
for i in d:
  i = round(float(i))
  if i not in bucket:
    bucket.append(i)

# Map to notes
print("Note mapping..")
notes = []
for i in bucket:
  for note in NOTES_MAP:
    note_freq = NOTES_MAP[note]

    l_r = i - 4
    h_r = i + 4
    if l_r < note_freq and h_r > note_freq:
      notes.append(note)
      break

print("Mapped Notes: {}".format(notes))

#========================================================Lilypond part
lilypond_notes = [pitch_to_lilypond(n) for n in notes]
note_string = ' '.join(lilypond_notes)

print("Generated lilypond notes: {}".format(note_string))

# === Step 3: Write to LilyPond file ===
ly_content = f"""
\\version "2.22.2"

\\score {{
  \\new Staff {{
    \\clef bass
    \\time 4/4
    \\tempo 4 = 80

    {note_string}
  }}
  \\layout {{ }}
}}
"""

with open("output.ly", "w") as f:
    f.write(ly_content)

print("✅ LilyPond file written as 'output.ly'")

# === Step 4: Compile to PDF using LilyPond ===
end = time.time()
try:
    subprocess.run(["C:\\LilyPond\\usr\\bin\\lilypond.exe", "output.ly"], check=True)
    print("✅ PDF generated as 'output.pdf'")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    
print("Execution Time: {}".format(end))