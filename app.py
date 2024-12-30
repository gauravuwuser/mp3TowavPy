import os
from flask import Flask, request, render_template, send_file, jsonify
from pydub import AudioSegment, silence
from io import BytesIO
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if a file was uploaded
        if "file" not in request.files:
            return "No file part in the request", 400
        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400

        # Save uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Process the uploaded MP3 file
        output_zip_path = process_audio(filepath)

        # Send the ZIP file for download
        return send_file(output_zip_path, as_attachment=True)

    # Render the upload form
    return render_template("upload.html")


def process_audio(filepath):
    # Load audio file
    audio = AudioSegment.from_file(filepath, format="mp3")

    # Convert to WAV, mono, 22050 Hz
    audio = audio.set_channels(1).set_frame_rate(22050)

    # Split audio based on silence
    min_silence_len = 350  # 0.35 seconds in milliseconds
    silence_thresh = -37   # Silence threshold in dB
    chunks = silence.split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=300  # Include some silence before/after
    )

    # Prepare to save chunks as WAV files
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for i, chunk in enumerate(chunks):
            chunk_filename = f"chunk_{i + 1}.wav"
            chunk_path = os.path.join(PROCESSED_FOLDER, chunk_filename)
            chunk.export(chunk_path, format="wav")
            zip_file.write(chunk_path, chunk_filename)

    # Cleanup temporary files
    for file in os.listdir(PROCESSED_FOLDER):
        os.remove(os.path.join(PROCESSED_FOLDER, file))

    # Save the ZIP archive
    zip_buffer.seek(0)
    output_zip_path = os.path.join(UPLOAD_FOLDER, "processed_chunks.zip")
    with open(output_zip_path, "wb") as f:
        f.write(zip_buffer.getvalue())

    return output_zip_path


if __name__ == "__main__":
    app.run(debug=False)
