from flask import Flask, Response, render_template
import cv2
from pandas.io.sas.sas_constants import subheader_count_length

import config

app = Flask(__name__)

class TestCamera:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)

    def __del__(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()


    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

def getnerate_frames(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    camera = TestCamera(config.Config.streaming_source)
    return Response(getnerate_frames(camera),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=config.Config.DEBUG, host=config.Config.HOST, port=config.Config.PORT)