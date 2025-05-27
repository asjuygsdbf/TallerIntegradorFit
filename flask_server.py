from flask import Flask, request, Response, jsonify
import cv2
import numpy as np
from utils import get_mediapipe_pose
from core.processor_router import get_processor
from core.thresholds_squat import get_thresholds_squat_beginner
from core.thresholds_pushup import get_thresholds_pushup_beginner

app = Flask(__name__)
pose = get_mediapipe_pose()
latest_frame = None

@app.route('/video_stream_upload', methods=['POST'])
def receive_frame():
    global latest_frame

    ejercicio = request.args.get("ejercicio", "sentadilla")  # default: sentadilla
    file = request.data
    frame = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
    if frame is None:
        return jsonify({"error": "Frame inválido"}), 400

    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Elegir umbrales según ejercicio
    if ejercicio == "flexion":
        thresholds = get_thresholds_pushup_beginner()
    elif ejercicio == "abdominal":
        thresholds = get_thresholds_abdominal_beginner()
    else:
        thresholds = get_thresholds_squat_beginner()
        
    processor = get_processor(ejercicio, thresholds, flip_frame=True)
    processed_frame, _ = processor.process(frame_rgb, pose)

    frame_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
    latest_frame = frame_bgr
    return jsonify({"status": "ok"}), 200

@app.route('/view_stream')
def view_stream():
    def generate():
        while True:
            if latest_frame is not None:
                ret, buffer = cv2.imencode('.jpg', latest_frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
