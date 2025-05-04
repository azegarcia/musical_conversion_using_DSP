import subprocess

# === Step 1: Your list of notes ===
notes = ['B5', 'B5', 'G2', 'G2', 'B5', 'B5', 'B5', 'B5', 'B5', 'B5', 'G2', 'G2', 'F#2', 'F#2', 'F#2', 'A#5', 'A#5', 'A#5', 'A#5', 'A#5', 'A#5', 'A#5', 'F#2', 'A#5', 'F#2', 'F2', 'F2', 'F2', 'A5', 'A5', 'A5', 'A5', 'F2', 'A5', 'A5', 'A5', 'F2', 'E2', 'E2', 'E2', 'G#5', 'G#5', 'G#5', 'G#5', 'G#5', 'E2', 'G#5', 'G#5', 'G#5', 'E2', 'D#2', 'D#2', 'D#2', 'G5', 'G5', 'G5', 'G5', 'G5', 'G5', 'G5', 'G5', 'D#2', 'D2', 'D2', 'D2', 'F#5', 'F#5', 'F#5', 'F#5', 'D2', 'F#5', 'F#5', 'F#5', 'F#5', 'C#2', 'C#2', 'C#2', 'F5', 'F5', 'F5', 'C#2', 'F5', 'F5', 'F5', 'F5', 'F5', 'C2', 'C2', 'C2', 'E5', 'E5', 'E5', 'E5', 'C2', 'E5', 'E5', 'E5', 'E5', 'B1', 'B1', 'B1', 'D#5', 'D#5', 'D#5', 'D#5', 'D#5', 'D#5', 'D#5', 'A#1', 'D#5', 'A#1', 'A#1', 'D5', 'D5', 'A#1', 'D5', 'D5', 'D5', 'D5', 'D5', 'D5', 'A1', 'A1', 'A1', 'C#5', 'C#5', 'C#5', 'C#5', 'C#5', 'C#5', 'C#5', 'C#5', 'G#1', 'G#1', 'G#1', 'C5', 'C5', 'C5', 'C5', 'C5', 'C5', 'C5', 'C5', 'G1', 'G1', 'F#1', 'D#8', 'D#8', 'D#8', 'D#8', 'D#8', 'D#8', 'D#8', 'D#8', 'B4', 'B4', 'B4', 'B4', 'B4', 'B4', 'B4', 'B4', 'F#1', 'F#1', 'D8', 'D8', 'D8', 'A#4', 'F1', 'D8', 'D8', 'D8', 'D8', 'D8', 'A#4', 'A#4', 'A#4', 'A#4', 'A#4', 'A#4', 'A#4', 'F1', 'E1', 'C#8', 'C#8', 'C#8', 'C#8', 'C#8', 'C#8', 'C#8', 'C#8', 'A4', 'A4', 'A4', 'A4', 'E1', 'A4', 'A4', 'A4', 'E1', 'D#1', 'C8', 'G#4', 'C8', 'C8', 'C8', 'C8', 'C8', 'C8', 'C8', 'G#4', 'G#4', 'G#4', 'G#4', 'G#4', 'G#4', 'G#4', 'D#1', 'D1', 'B7', 'B7', 'B7', 'B7', 'B7', 'B7', 'G4', 'B7', 'B7', 'G4', 'G4', 'G4', 'G4', 'G4', 'D1', 'G4', 'C#1', 'A#7', 'A#7', 'A#7', 'A#7', 'F#4', 'A#7', 'A#7', 'A#7', 'A#7', 'F#4', 'F#4', 'F#4', 'C#1', 'F#4', 'F#4', 'F#4', 'F#4', 'C1', 'F4', 'A7', 'A7', 'A7', 'A7', 'F4', 'A7', 'A7', 'A7', 'F4', 'F4', 'C1', 'F4', 'F4', 'F4', 'F4', 'B0', 'E4', 'G#7', 'G#7', 'G#7', 'G#7', 'G#7', 'G#7', 'G#7', 'E4', 'G#7', 'E4', 'E4', 'A#0', 'E4', 'E4', 'E4', 'E4', 'A#0', 'D#4', 'D#4', 'G7', 'G7', 'G7', 'G7', 'G7', 'G7', 'G7', 'G7', 'D#4', 'D#4', 'D#4', 'D#4', 'A0', 'D#4', 'D#4', 'A0', 'D4', 'F#7', 'F#7', 'F#7', 'F#7', 'D4', 'F#7', 'F#7', 'F#7', 'F#7', 'D4', 'D4', 'D4', 'D4', 'D4', 'D4', 'G#0', 'C#4', 'C#4', 'G0', 'F7', 'F7', 'F7', 'F7', 'F7', 'F7', 'F7', 'F7', 'C#4', 'C#4', 'C#4', 'C#4', 'C#4', 'C#4', 'F#0', 'C4', 'E7', 'E7', 'C4', 'E7', 'E7', 'E7', 'E7', 'E7', 'E7', 'C4', 'C4', 'C4', 'C4', 'F#0', 'C4', 'C4', 'B3', 'F0', 'D#7', 'D#7', 'D#7', 'D#7', 'B3', 'D#7', 'D#7', 'D#7', 'D#7', 'B3', 'B3', 'B3', 'B3', 'B3', 'B3', 'E0', 'A#3', 'A#3', 'D7', 'D7', 'D7', 'D7', 'A#3', 'D7', 'D7', 'D7', 'D7', 'A#3', 'A#3', 'A#3', 'A#3', 'A#3', 'D#0', 'A3', 'C#7', 'C#7', 'A3', 'C#7', 'C#7', 'C#7', 'C#7', 'C#7', 'C#7', 'A3', 'A3', 'D0', 'A3', 'A3', 'A3', 'G#3', 'G#3', 'C#0', 'C7', 'C7', 'C7', 'C7', 'C7', 'C7', 'C7', 'G#3', 'G#3', 'G#3', 'G#3', 'G#3', 'G#3', 'C0', 'G3', 'G3', 'B6', 'B6', 'B6', 'B6', 'B6', 'B6', 'B6', 'B6', 'G3', 'G3', 'G3', 'G3', 'G3', 'C0', 'F#3', 'F#3', 'A#6', 'A#6', 'A#6', 'A#6', 'A#6', 'A#6', 'A#6', 'A#6', 'F#3', 'F#3', 'F#3', 'F#3', 'F#3', 'C0', 'F3', 'F3', 'A6', 'A6', 'A6', 'A6', 'F3', 'A6', 'A6', 'A6', 'F3', 'F3', 'F3', 'F3', 'F3', 'C0', 'E3', 'E3', 'G#6', 'G#6', 'G#6', 'G#6', 'G#6', 'G#6', 'E3', 'G#6', 'G#6', 'E3', 'E3', 'E3', 'E3', 'E3', 'C0', 'D#3', 'D#3', 'G6', 'G6', 'D#3', 'G6', 'G6', 'G6', 'G6', 'G6', 'G6', 'D#3', 'D#3', 'D#3', 'D#3', 'D#3', 'D3', 'C0', 'D3', 'F#6', 'F#6', 'F#6', 'F#6', 'D3', 'F#6', 'F#6', 'F#6', 'F#6', 'D3', 'D3', 'D3', 'D3', 'D3', 'C#3', 'C#3', 'F6', 'C#3', 'C0', 'F6', 'F6', 'F6', 'F6', 'F6', 'F6', 'F6', 'C#3', 'C#3', 'C#3', 'C#3', 'C#3', 'C3', 'C3', 'E6', 'E6', 'E6', 'C3', 'E6', 'E6', 'E6', 'E6', 'E6', 'C3', 'C3', 'C0', 'C3', 'C3', 'B2', 'B2', 'B2', 'D#6', 'D#6', 'D#6', 'D#6', 'D#6', 'D#6', 'D#6', 'D#6', 'B2', 'B2', 'B2', 'B2', 'A#2', 'A#2', 'A#2', 'D6', 'D6', 'D6', 'D6', 'D6', 'D6', 'D6', 'D6', 'A#2', 'A#2', 'A#2', 'A#2', 'A2', 'A2', 'C#6', 'C#6', 'C#6', 'A2', 'C#6', 'C#6', 'C#6', 'C#6', 'C#6', 'A2', 'A2', 'A2', 'G#2', 'G#2', 'C6', 'G#2', 'C6', 'C6', 'C6', 'C6', 'C6', 'C6', 'C6', 'G#2', 'G#2', 'G#2', 'G2']

# === Step 2: Convert to LilyPond format ===
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
try:
    subprocess.run(["C:\\LilyPond\\usr\\bin\\lilypond.exe", "output.ly"], check=True)
    print("✅ PDF generated as 'output.pdf'")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
