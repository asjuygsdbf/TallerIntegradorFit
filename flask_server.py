from flask import Flask, request, Response, jsonify
import cv2
import numpy as np
from process_frame import ProcessFrame
from utils import get_mediapipe_pose
import threading
import time

app = Flask(__name__)

# Inicialización del modelo
thresholds = {
    'HIP_KNEE_VERT': {
        'NORMAL': (0, 32),
        'TRANS': (35, 65),
        'PASS': (70, 95)
    },
    'HIP_THRESH': [10, 50],
    'ANKLE_THRESH': 45,
    'KNEE_THRESH': [50, 70, 95],
    'OFFSET_THRESH': 35.0,
    'INACTIVE_THRESH': 15.0,
    'CNT_FRAME_THRESH': 50
}

pose = get_mediapipe_pose()
process_frame = ProcessFrame(thresholds=thresholds, flip_frame=True)

# Frame procesado más reciente
latest_frame = None
lock = threading.Lock()

@app.route('/video_stream_upload', methods=['POST'])
def receive_frame():
    global latest_frame
    file = request.data  # Usamos request.data en lugar de request.get_data()

    frame = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
    if frame is None:
        return jsonify({"error": "Frame inválido"}), 400

    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    processed_frame, _ = process_frame.process(frame_rgb, pose)
    frame_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)

    with lock:
        latest_frame = frame_bgr

    return jsonify({"status": "ok"}), 200

@app.route('/view_stream')
def view_stream():
    def generate():
        while True:
            frame = None
            with lock:
                if latest_frame is not None:
                    frame = latest_frame.copy()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                time.sleep(0.01)

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
