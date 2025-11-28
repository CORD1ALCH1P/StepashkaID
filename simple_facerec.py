import face_recognition
import cv2
import os


class simple_facerec:
    def __init__(self):
        self.encodings = []
        self.names = []

    def load_encoding_images(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                path = os.path.join(folder_path, filename)
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    self.encodings.append(encoding[0])
                    self.names.append(os.path.splitext(filename)[0])

    def detect_known_faces(self, frame):
        rgb_frame = frame[:, :, ::-1]  # BGR to RGB
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        names = []
        for encoding in face_encodings:
            matches = face_recognition.compare_faces(self.encodings, encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = self.names[first_match_index]

            names.append(name)

        return face_locations, names