from flask import Flask, Response, render_template_string
import cv2
import os
from main import FaceRecognizer
from PIL import Image
import io
from config import config

app = Flask(__name__)

# выбор источника
VIDEO_SOURCE = config.streaming_source
try:
    VIDEO_SOURCE = int(VIDEO_SOURCE)
except ValueError:
    pass

print(f"Открытие видеопотока: {VIDEO_SOURCE}")

camera = cv2.VideoCapture(VIDEO_SOURCE)

if isinstance(VIDEO_SOURCE, str) and "rtsp" in VIDEO_SOURCE.lower():
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not camera.isOpened():
    print(f"ОШИБКА: Не удалось открыть видеопоток: {VIDEO_SOURCE}")
    exit(1)

print(f"Видеопоток открыт: {VIDEO_SOURCE}")

recognizer = FaceRecognizer()

def frame_to_jpeg(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()

def gen_frames():
    # Прогрев камеры
    for _ in range(10):
        camera.grab()

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Кадр не прочитан — пытаюсь переподключиться...")
            camera.release()
            camera.open(VIDEO_SOURCE)
            continue

        frame = recognizer.process_frame(frame)
        jpeg = frame_to_jpeg(frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.HOST, debug=config.DEBUG, threaded=True)