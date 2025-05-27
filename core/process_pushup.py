import numpy as np
import cv2
from utils import find_angle, get_landmark_features, draw_text

class PushUpProcessor:
    def __init__(self, thresholds, flip_frame=False):
        self.thresholds = thresholds
        self.flip_frame = flip_frame
        self.state = "up"
        self.counter = 0
        self.incorrect_form = 0

        self.COLORS = {
            'red': (255, 80, 80),
            'orange': (255, 153, 0),
            'green': (18, 185, 0)
        }

    def process(self, frame, pose):
        frame_height, frame_width, _ = frame.shape
        frame_output = frame.copy()
        play_sound = None

        results = pose.process(frame)
        if results.pose_landmarks:
            keypoints = results.pose_landmarks.landmark

            # Obtener puntos clave
            left_shldr, left_elbow, left_wrist = get_landmark_features(keypoints, 'left', frame_width, frame_height)[:3]
            right_shldr, right_elbow, right_wrist = get_landmark_features(keypoints, 'right', frame_width, frame_height)[:3]
            left_hip = get_landmark_features(keypoints, 'left', frame_width, frame_height)[3]
            right_hip = get_landmark_features(keypoints, 'right', frame_width, frame_height)[3]
            left_ankle = get_landmark_features(keypoints, 'left', frame_width, frame_height)[5]
            right_ankle = get_landmark_features(keypoints, 'right', frame_width, frame_height)[5]

            # Ángulo del codo
            angle_elbow_left = find_angle(left_shldr, left_elbow, left_wrist)
            angle_elbow_right = find_angle(right_shldr, right_elbow, right_wrist)
            elbow_angle = (angle_elbow_left + angle_elbow_right) / 2

            # Alineación cadera
            shoulder_y = (left_shldr[1] + right_shldr[1]) / 2
            hip_y = (left_hip[1] + right_hip[1]) / 2
            ankle_y = (left_ankle[1] + right_ankle[1]) / 2
            align_offset = (hip_y - ((shoulder_y + ankle_y) / 2)) / (ankle_y - shoulder_y)

            form_ok = True

            # Feedback visual
            if elbow_angle > self.thresholds['MIN_ELBOW_FLEXION_FOR_COUNT']:
                draw_text(frame_output, "¡BAJA MÁS LOS CODOS!", pos=(30, 230), text_color_bg=self.COLORS['red'])
                form_ok = False

            if abs(align_offset) > self.thresholds['MAX_FORM_DEVIATION_OFFSET']:
                draw_text(frame_output, "¡MANTÉN EL CUERPO RECTO!", pos=(30, 280), text_color_bg=self.COLORS['orange'])
                form_ok = False

            # Contador de repeticiones
            if elbow_angle <= self.thresholds['MIN_ELBOW_FLEXION_FOR_COUNT'] and self.state == "up":
                self.state = "down"
            elif elbow_angle >= self.thresholds['MAX_ELBOW_EXTENSION_FOR_COUNT'] and self.state == "down":
                if form_ok:
                    self.counter += 1
                    play_sound = str(self.counter)
                else:
                    self.incorrect_form += 1
                    play_sound = "INCORRECTA"
                self.state = "up"

            # Mostrar textos
            draw_text(frame_output, f"FLEXIONES CORRECTAS: {self.counter}", pos=(30, 30), text_color_bg=self.COLORS['green'])
            draw_text(frame_output, f"INCORRECTAS: {self.incorrect_form}", pos=(30, 80), text_color_bg=self.COLORS['red'])
            draw_text(frame_output, f"ÁNGULO CODO: {int(elbow_angle)}", pos=(30, 130), text_color_bg=self.COLORS['orange'])
            draw_text(frame_output, f"ALINEACIÓN: {round(align_offset, 2)}", pos=(30, 180), text_color_bg=self.COLORS['orange'])

        if self.flip_frame:
            frame_output = cv2.flip(frame_output, 1)

        return frame_output, play_sound