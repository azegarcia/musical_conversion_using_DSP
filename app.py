from flask import Flask, request, render_template_string, send_file
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import scipy.io.wavfile as wav
import json
from music21 import stream, note, chord, midi, converter
import tempfile

# Load notes mapping once
NOTES_MAP = json.load(open("notes_map.json", "r"))

app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML Template
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>WAV to MIDI and Sheet</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-5">
  <div class="row justify-content-center">
    <div class="col-lg-6">
      <div class="card shadow">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Upload a WAV File</h2>
          <form method="POST" enctype="multipart/form-data">
            <div class="mb-3">
              <input class="form-control" type="file" name="file" accept=".wav" required>
            </div>
            <div class="d-grid">
              <button class="btn btn-primary" type="submit">Upload & Process</button>
            </div>
          </form>
          {% if message %}
          <div class="alert alert-info mt-4">{{ message|safe }}</div>
          {% endif %}
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
'''

# Core function to process WAV
def process_wav(file_path, output_dir):
    DURATION = 300  # in seconds

    SAMPLE_RATE, data = wav.read(file_path)

    # Plot time domain
    t = 1 * np.arange(SAMPLE_RATE * DURATION)
    # plt.figure()
    plt.plot(t, data[:SAMPLE_RATE * DURATION])
    plt.title('Magnitude over Time')
    plt.savefig(os.path.join(output_dir, 'magnitude.png'))
    plt.close()

    # FFT and frequency domain plot
    yf = fft(data[:SAMPLE_RATE * DURATION])
    xf = fftfreq(SAMPLE_RATE * DURATION, 1 / SAMPLE_RATE)
    # plt.figure()
    plt.plot(xf, np.abs(yf))
    plt.xlim([0, 3000])
    plt.title('Frequency Spectrum')
    plt.savefig(os.path.join(output_dir, 'frequency.png'))
    plt.close()

    # Map frequencies to magnitude
    y = np.abs(yf)
    d = {xf[i]: y[i] for i in range(len(y)) if xf[i] > 0}
    d = sorted(d, reverse=True)

    # Top notes
    bucket = []
    for freq, _ in d:
        freq_rounded = round(freq)
        if freq_rounded not in bucket:
            bucket.append(freq_rounded)

    notes_found = []
    for freq in bucket:
        for note_name, note_freq in NOTES_MAP.items():
            if freq - 4 < note_freq < freq + 4:
                notes_found.append(note_name)
                break

    # Create chord
    s = stream.Stream()
    c = chord.Chord(list(set(notes_found)))
    c.quarterLength = 2
    s.append(c)

    # Save MIDI
    midi_file_path = os.path.join(output_dir, 'audio_output.mid')
    mf = midi.translate.streamToMidiFile(s)
    mf.open(midi_file_path, 'wb')
    mf.write()
    mf.close()

    # Save MusicXML
    midi_stream = converter.parse(midi_file_path)
    xml_file_path = os.path.join(output_dir, 'output.xml')
    midi_stream.write('musicxml', fp=xml_file_path)

    return midi_file_path, xml_file_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = None
    if request.method == 'POST':
        if 'file' not in request.files:
            message = "No file uploaded."
        else:
            file = request.files['file']
            if file.filename == '':
                message = "No file selected."
            elif file and file.filename.endswith('.wav'):
                # Save uploaded file temporarily
                temp_dir = tempfile.mkdtemp()
                temp_path = os.path.join(temp_dir, file.filename)
                file.save(temp_path)

                try:
                    midi_path, xml_path = process_wav(temp_path, UPLOAD_FOLDER)
                    message = f'Processing complete!<br>' \
                              f'<a href="/download/midi">Download MIDI</a><br>' \
                              f'<a href="/download/xml">Download MusicXML</a><br>' \
                              f'<img src="/static/magnitude.png" class="img-fluid mt-3"><br>' \
                              f'<img src="/static/frequency.png" class="img-fluid mt-3">'
                except Exception as e:
                    message = f"An error occurred: {e}"

    return render_template_string(HTML_TEMPLATE, message=message)

@app.route('/download/<filetype>')
def download_file(filetype):
    if filetype == 'midi':
        return send_file(os.path.join(UPLOAD_FOLDER, 'audio_output.mid'), as_attachment=True)
    elif filetype == 'xml':
        return send_file(os.path.join(UPLOAD_FOLDER, 'output.xml'), as_attachment=True)
    else:
        return "Invalid download type.", 400

if __name__ == '__main__':
    app.run(debug=True)
