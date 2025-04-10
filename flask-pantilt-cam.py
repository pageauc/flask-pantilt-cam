#!/usr/bin/python3
from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import Transform
import pantilthat
import os
import io
import threading
from datetime import datetime
from config import Config

prog_ver = "1.0"

app = Flask(__name__)

config = Config() # Load Variables from config.py file class Config()
# create absolute path for snapshot images folder
image_folder = os.path.abspath(config.IM_SNAP_FILEPATH)
os.makedirs(image_folder, exist_ok=True)  # create folder path if it does not exist
print(f"flask-pantilt-cam.py ver {prog_ver}")
print(f"INFO : Images will be saved to {image_folder}")

# ===== PAN-TILT INIT =====
pantilthat.pan(0)
pantilthat.tilt(0)
pantilthat.idle_timeout(0.1)
current_pan = 0
current_tilt = 0

# flip pan tilt controls to match flipped image
if config.IM_HFLIP:
    left = 'right'
    right = 'left'
else:
    left = 'left'
    right = 'right'

if config.IM_VFLIP:
    up = 'down'
    down = 'up'
else:
    up = 'up'
    down = 'down'

# ===== CAMERA INITIALIZATION =====
picam2 = Picamera2()
video_config = picam2.create_video_configuration(
    main={"size": (config.IM_WIDTH, config.IM_HEIGHT)},
    transform=Transform(hflip=config.IM_HFLIP, vflip=config.IM_VFLIP)
)
picam2.configure(video_config)

still_config = picam2.create_still_configuration(
    main={"size": (config.IM_SNAP_WIDTH, config.IM_SNAP_HEIGHT)},
    transform=Transform(hflip=config.IM_HFLIP, vflip=config.IM_VFLIP)
)

# ===== STREAMING HANDLER =====
class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        super().__init__()
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

output = StreamingOutput()

def generate_frames():
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def capture_photo():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{config.IM_SNAP_PREFIX}-{timestamp}.jpg"
    filepath = os.path.join(image_folder, filename)

    picam2.stop_recording()
    picam2.switch_mode(still_config)
    picam2.capture_file(filepath)
    picam2.switch_mode(video_config)
    picam2.start_recording(JpegEncoder(), FileOutput(output))

    return filename

# ===== ROUTES =====
@app.route('/')
def index():
    return render_template('index.html',
                         title=config.WEB_TITLE,
                         photos_dir=image_folder)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                  mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/photos/<filename>')
def serve_photo(filename):
    return send_from_directory(image_folder, filename)

@app.route('/control', methods=['POST'])
def control():
    global current_pan, current_tilt

    data = request.json
    direction = data.get('direction')

    if direction == down:
        current_tilt = min(90, current_tilt + config.TILT_SPEED)
    elif direction == up:
        current_tilt = max(-90, current_tilt - config.TILT_SPEED)
    elif direction == left:
        current_pan = max(-90, current_pan - config.PAN_SPEED)
    elif direction == right:
        current_pan = min(90, current_pan + config.PAN_SPEED)
    elif direction == 'center':
        current_pan = 0
        current_tilt = 0

    pantilthat.pan(current_pan)
    pantilthat.tilt(current_tilt)

    return jsonify({'pan': current_pan, 'tilt': current_tilt})

@app.route('/capture', methods=['POST'])
def capture():
    try:
        filename = capture_photo()
        return jsonify({
            'status': 'success',
            'filename': filename,
            'url': f'/photos/{filename}'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_image/<filename>')
def get_image(filename):
    return send_from_directory(image_folder, filename)

@app.route('/browse')
def browse():
    """Photo browser interface"""
    try:
        path = os.path.abspath(request.args.get('directory', image_folder))
        if not path.startswith(os.path.abspath(image_folder)):
            path = image_folder

        page = int(request.args.get('page', 1))

        files = sorted([
            f for f in os.listdir(path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
            and os.path.isfile(os.path.join(path, f))
        ], reverse=True)

        # Pagination
        total_pages = (len(files) + config.PHOTOS_PER_PAGE - 1) // config.PHOTOS_PER_PAGE
        start_idx = (page - 1) * config.PHOTOS_PER_PAGE
        paginated_files = files[start_idx:start_idx + config.PHOTOS_PER_PAGE]

        return render_template('browse-dir.html',
                            files=paginated_files,
                            current_dir=path,
                            current_page=page,
                            total_pages=total_pages,
                            title=f"Photos - {config.WEB_TITLE}")

    except Exception as e:
        return f"Error browsing directory: {str(e)}", 400

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Create static directories if they don't exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)

    # Start frame capture
    picam2.start_recording(JpegEncoder(), FileOutput(output))

    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    finally:
        picam2.stop_recording()
        pantilthat.pan(0)
        pantilthat.tilt(0)
