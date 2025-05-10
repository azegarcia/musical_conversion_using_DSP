import os
import json
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import numpy as np
import scipy.io.wavfile as wav
from scipy.fft import fft, fftfreq
from music21 import *
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI operations
import matplotlib.pyplot as plt

environment.UserSettings()['lilypondPath'] =  'C:/LilyPond/usr/bin/lilypond.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'webm'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def ensure_wav_format(input_path):
    ext = input_path.rsplit('.', 1)[-1].lower()
    if ext == 'wav':
        return input_path  # Already WAV
    audio = AudioSegment.from_file(input_path)
    wav_path = input_path.rsplit('.', 1)[0] + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

# Check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pitch_to_lilypond(note):
    base_map = {'C': 'c', 'D': 'd', 'E': 'e', 'F': 'f', 'G': 'g', 'A': 'a', 'B': 'b'}
    accidental_map = {'#': 'is', 'b': 'es'}
    
    if len(note) == 2:
        pitch, octave = note[0], int(note[1])
        accidental = ''
    else:
        pitch, accidental, octave = note[0], note[1], int(note[2])
        accidental = accidental_map.get(accidental, '')

    lily_note = base_map[pitch] + accidental
    offset = octave - 3
    lily_note += "'" * offset if offset > 0 else "," * abs(offset)
    return lily_note + "4"

def identify_instrument(instrument):
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

def identify_clef(instrument):
    if instrument == "Flute":
        clef = "clef treble"
    elif instrument == "Piano":
        clef = "clef treble"
    elif instrument == "Saxophone":
        clef = "clef treble"
    elif instrument == "Bass":
        clef = "clef bass"
    else:
        clef = "clef treble"
        
    return clef

def insert_line_breaks(note_list, notes_per_line=8):
    lines = []
    for i in range(0, len(note_list), notes_per_line):
        chunk = ' '.join(note_list[i:i+notes_per_line])
        lines.append(chunk + " \\break")
    return '\n'.join(lines)

def process_audio(filepath, instrument):
    notes_map_file = identify_instrument(instrument)
    NOTES_MAP = json.load(open(notes_map_file, "r"))
    
    print("Reading wav file..")
    SAMPLE_RATE, data = wav.read(filepath)

    # If stereo, convert to mono by averaging channels
    if len(data.shape) > 1:
        data = data.mean(axis=1)

    DURATION = len(data) / SAMPLE_RATE  # Duration in seconds
    t = np.linspace(0., DURATION, len(data))  # Time axis

    print("Plotting magnitudes..")
    plt.figure(figsize=(10, 4))
    plt.plot(t, data)
    plt.title("Waveform")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig('static/magnitude.png')
    plt.close()

    # Perform FFT
    yf = fft(data)
    xf = fftfreq(len(data), 1 / SAMPLE_RATE)

    print("Plotting frequencies..")
    plt.figure(figsize=(10, 4))
    plt.plot(xf[:len(xf)//2], np.abs(yf[:len(yf)//2]))  # Only positive frequencies
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")
    plt.xlim([0, 3000])  # Limit to 3 kHz for visibility
    plt.tight_layout()
    plt.savefig('static/frequency.png')
    plt.close()

    print("Sorting frequencies..")
    y = np.abs(yf[:len(yf)//2])
    x = xf[:len(xf)//2]

    freq_magnitude_pairs = list(zip(x, y))
    freq_magnitude_pairs = sorted(freq_magnitude_pairs, key=lambda pair: pair[1], reverse=True)

    bucket = []
    for freq, _ in freq_magnitude_pairs:
        val = round(freq)
        if val > 0 and val not in bucket:
            bucket.append(val)
        if len(bucket) >= 100:  # Limit number of frequencies to map
            break

    print("Mapping notes..")
    notes = []
    for i in bucket:
        for note in NOTES_MAP:
            note_freq = NOTES_MAP[note]
            if abs(i - note_freq) <= 4:
                notes.append(note)
                break
    
    print("Notes mapped: {}".format(notes))
    lilypond_notes = [pitch_to_lilypond(n) for n in notes]
    note_string = insert_line_breaks(lilypond_notes, notes_per_line=12)

    title = os.path.splitext(os.path.basename(filepath))[0]
    clef = identify_clef(instrument)
    ly_content = f"""
    \\version "2.22.2"
    \\header {{
        title = "{title}"
        subtitle = "Instrument: {instrument}"
        composer = ""
        arranger = ""
        opus = "Op. 1"
        }}
        \\score {{
            \\new Staff {{
                \\{clef}
                \\time 4/4
                \\tempo 4 = 80
                {note_string}
            }}
            \\layout {{
                \\override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/4)
            }}
        }}
    """

    with open("output.ly", "w") as f:
        f.write(ly_content)

    try:
        subprocess.run(["C:\\LilyPond\\usr\\bin\\lilypond.exe", "output.ly"], check=True)
        return "output.pdf"
    except subprocess.CalledProcessError as e:
        print(f"Lilypond generation failed: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    instrument = request.form.get('instrument')

    if not file or file.filename == '' or not allowed_file(file.filename):
        return "Invalid file", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Convert to WAV regardless of format
    filepath = ensure_wav_format(filepath)

    pdf = process_audio(filepath, instrument)
    if pdf:
        return redirect(url_for('result'))
    else:
        return "Error generating PDF", 500

@app.route('/result')
def result():
    return render_template('result.html', pdf_file='output.pdf')

@app.route('/pdf/<filename>')
def serve_pdf(filename):
    return send_file(filename, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
