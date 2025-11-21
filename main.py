from deepface.models import face_detection

import WebGUI
import config
import threading
import cv2
from deepface import DeepFace
from config import *

cap = cv2.VideoCapture(config.streaming_source)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.streaming_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.streaming_height)
