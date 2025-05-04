import os
import json
import time
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import numpy as np
import scipy.io.wavfile as wav
from scipy.fft import fft, fftfreq
from music21 import *
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
    return {
        "Bass": "bass_map.json",
        "Flute": "flute_map.json",
        "Piano": "notes_map.json",
        "Saxophone": "saxo_map.json",
        "Violin": "violin_map.json"
    }.get(instrument, "notes_map.json")

def process_audio(filepath, instrument):
    environment.UserSettings()['lilypondPath'] =  'C:/LilyPond/usr/bin/lilypond.exe'

    notes_map_file = identify_instrument(instrument)
    NOTES_MAP = json.load(open(notes_map_file, "r"))
    
    SAMPLE_RATE, data = wav.read(filepath)
    DURATION = len(data) // SAMPLE_RATE

    t = np.arange(SAMPLE_RATE * DURATION)
    plt.plot(t, data[:SAMPLE_RATE*DURATION])
    plt.savefig('static/magnitude.png')
    plt.close()

    yf = fft(data[:SAMPLE_RATE*DURATION])
    xf = fftfreq(SAMPLE_RATE*DURATION, 1 / SAMPLE_RATE)
    plt.plot(xf, np.abs(yf))
    plt.xlim([0, 3e3])
    plt.savefig('static/frequency.png')
    plt.close()

    y = np.abs(yf)
    d = {f"{xf[i]}": y[i] for i in range(len(y)) if xf[i] > 0}
    d = sorted(d, key=lambda x: float(x), reverse=True)

    bucket = []
    for i in d:
        val = round(float(i))
        if val not in bucket:
            bucket.append(val)

    notes = []
    for freq in bucket:
        for note, note_freq in NOTES_MAP.items():
            if freq - 4 < note_freq < freq + 4:
                notes.append(note)
                break

    lilypond_notes = [pitch_to_lilypond(n) for n in notes]
    note_string = ' '.join(lilypond_notes)

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

    try:
        subprocess.run(["C:\\LilyPond\\usr\\bin\\lilypond.exe", "output.ly"], check=True)
        return "output.pdf"
    except subprocess.CalledProcessError:
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
