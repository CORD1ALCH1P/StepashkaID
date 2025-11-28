import os
import cv2
import face_recognition
import pickle
import numpy as np
import subprocess
from datetime import datetime


class FaceRecognizer:
    def __init__(self, known_dir="./known_persons", pkl_file="known_persons.pkl", train_script="train.py"):
        self.known_dir = known_dir
        self.pkl_file = pkl_file
        self.train_script = train_script

        self.known_face_encodings = []
        self.known_face_names = []

        self._load_or_train()

    def _need_retrain(self):
        if not os.path.exists(self.pkl_file):
            return True
        pkl_time = os.path.getmtime(self.pkl_file)
        for root, _, files in os.walk(self.known_dir):
            for f in files:
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    if os.path.getmtime(os.path.join(root, f)) > pkl_time:
                        return True
        return False

    def _load_or_train(self):
        print("Загрузка базы известных лиц...", end=" ")
        if self._need_retrain():
            print("\nБаза устарела → переобучаю...")
            result = subprocess.run(["python", self.train_script], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Ошибка обучения:\n{result.stderr}")
            print("Переобучение завершено")

        with open(self.pkl_file, "rb") as f:
            data = pickle.load(f)
            self.known_face_encodings = data["encodings"]
            self.known_face_names = data["names"]

        print(f"Загружено {len(self.known_face_encodings)} encodings "
              f"({len(set(self.known_face_names))} человек(а))")

    def process_frame(self, frame):
        """
        Принимает BGR-кадр от OpenCV, возвращает тот же кадр с нарисованными рамками и именами
        """
        small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, locations)

        for (top, right, bottom, left), enc in zip(locations, encodings):
            top, right, bottom, left = top*2, right*2, bottom*2, left*2

            # Поиск совпадения
            distances = face_recognition.face_distance(self.known_face_encodings, enc)
            matches = face_recognition.compare_faces(self.known_face_encodings, enc, tolerance=0.5)

            name = "Неизвестный"
            color = (0, 0, 255)

            if len(distances) > 0:
                best_idx = np.argmin(distances)
                if matches[best_idx]:
                    name = self.known_face_names[best_idx]
                    color = (0, 255, 0)

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # Информация в углу
        info = f"Людей: {len(locations)} | {datetime.now():%H:%M:%S}"
        cv2.putText(frame, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        return frame