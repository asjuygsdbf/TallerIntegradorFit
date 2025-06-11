from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import os
import uuid

from utils import get_mediapipe_pose
from core.processor_router import get_processor
from core.thresholds_squat import get_thresholds_squat_beginner
from core.thresholds_pushup import get_thresholds_pushup_beginner
from core.thresholds_abdominal import get_thresholds_abdominal_beginner

app = Flask(__name__)
pose = get_mediapipe_pose()

@app.route('/analyze', methods=['POST'])
def analyze_frame():
    ejercicio = request.args.get("ejercicio", "sentadilla")
    image_bytes = request.data
    tmp_filename = f"/tmp/frame_{uuid.uuid4().hex}.jpg"

    try:
        with open(tmp_filename, "wb") as f:
            f.write(image_bytes)

        image = Image.open(tmp_filename).convert("RGB")
        frame_rgb = np.array(image)

        if ejercicio == "flexion":
            thresholds = get_thresholds_pushup_beginner()
        elif ejercicio == "abdominal":
            thresholds = get_thresholds_abdominal_beginner()
        else:
            thresholds = get_thresholds_squat_beginner()

        processor = get_processor(ejercicio, thresholds, flip_frame=False)
        _, feedback = processor.process(frame_rgb, pose)

        return jsonify({
            "ejercicio": ejercicio,
            "feedback": feedback or "Sin feedback",
            "status": "ok"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
