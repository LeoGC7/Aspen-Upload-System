from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# Set the folder to store uploaded videos
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the maximum upload size to 1GB (or any size you want)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024  # 1 GB in bytes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No file uploaded", 400

    video = request.files['video']

    if video.filename == '':
        return "No file selected", 400

    # Save the video to the upload folder
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    video.save(video_path)

    return f"Video uploaded successfully! Saved to: {video_path}"

@app.route('/upload_success')
def upload_success():
    return "Video uploaded successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)