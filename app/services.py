import cv2
import numpy as np
from typing import List, Dict


class VideoAnalyzer:
    """
    Простейший прототип видеоанализатора.
    Здесь можно позже подключить ML-модели (например, YOLO, DeepSort и т.д.).
    """

    def __init__(self, boundary_area: tuple[int, int, int, int] = (100, 100, 400, 400)):
        # Прямоугольная "зона контроля" — (x1, y1, x2, y2)
        self.boundary_area = boundary_area

    def analyze(self, video_path: str) -> List[Dict]:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("Не удалось открыть видеофайл")

        frame_count = 0
        violations = []
        x1, y1, x2, y2 = self.boundary_area

        # Простая имитация анализа: смотрим разницу между кадрами
        ret, prev_frame = cap.read()
        if not ret:
            return []

        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(prev_gray, gray)
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

            # Проверяем "движение" в зоне
            zone = thresh[y1:y2, x1:x2]
            movement = np.sum(zone) / 255

            if movement > 500:  # пороговое значение
                violations.append({
                    "frame": frame_count,
                    "type": "movement_in_restricted_zone",
                    "confidence": round(min(movement / 10000, 1.0), 2)
                })

            prev_gray = gray

        cap.release()
        return violations
