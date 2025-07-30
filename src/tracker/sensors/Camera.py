import cv2
import threading
from ultralytics import YOLO

from .. import Globals
from .. import ProccessSensorData

# ===============================
# MODEL CONFIGURATION
# ===============================

MODEL_PATH = "models/best.pt"
DEVICE = "cuda:0"

# ===============================
# VIDEO SOURCE CONFIGURATION
# ===============================

CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# ===============================
# PREDICTION PARAMETERS
# ===============================

CONFIDENCE_THRESHOLD = 0.1
IOU_THRESHOLD = 0.8
IMAGE_SIZE = 416

SHOW_VIDEO = True  # Set to False to disable OpenCV window
CLASSES_TO_DETECT = None  # Or [Globals.ClassID] if restricting detection

# ===============================
# MODEL INITIALIZATION
# ===============================

model = YOLO(MODEL_PATH)
model.to(DEVICE)

# ===============================
# DETECTION LOOP
# ===============================

def DetectionLoop():
    print("Camera Being Initialized")
    
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        print("❌ Failed to open video source.")
        return

    while Globals.Mode == "Camera" and not Globals.SensorStopEvent.is_set():
        ret, frame = cap.read()
        if not ret:
            continue

        results = model.predict(
            source=frame,
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,
            classes=CLASSES_TO_DETECT,
            device=DEVICE,
            imgsz=IMAGE_SIZE,
            verbose=False,
            stream=False,
        )

        result = results[0]
        detected = False
        for box in result.boxes:
            cls_id = int(box.cls[0])
            if CLASSES_TO_DETECT is None or cls_id == CLASSES_TO_DETECT:
                detected = True
                break

        # Immediately send the detection state
        ProccessSensorData.SensorData(detected)

        # Optionally display annotated frame
        if SHOW_VIDEO:
            frame_with_boxes = result.plot()
            cv2.imshow("YOLOv8 Detection", frame_with_boxes)
            if cv2.waitKey(1) in [27, ord('q')]:  # ESC or Q to quit display
                break

    cap.release()
    cv2.destroyAllWindows()


