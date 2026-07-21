import cv2
import time
import os
from datetime import datetime
from ultralytics import YOLO
from backend.database import log_violation, init_db

from backend.config import (
    MODEL_PATH, VIDEO_PATH, SNAP_DIR, COOLDOWN,
    CLASS_CONF, CLASS_NAMES, VIOLATION_CLASSES, ZONES, CONF_THRESH
)

from backend.api import frame_store


# ─── Helpers ───────────────────────────────────────────────────────────────────
def get_zone(x_center: int, frame_width: int) -> str:
    ratio = x_center / frame_width
    idx   = min(int(ratio * len(ZONES)), len(ZONES) - 1)
    return ZONES[idx]


def save_snapshot(frame, violation_type: str) -> str:
    os.makedirs(SNAP_DIR, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = f"{SNAP_DIR}/{violation_type.replace(' ', '_')}_{ts}.jpg"
    cv2.imwrite(path, frame)
    return path



def draw_violation_banner(frame, violations: list):
    if not violations:
        return frame
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], 52), (0, 0, 180), -1)
    cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)
    text = f"VIOLATION: {', '.join(set(violations))}"
    cv2.putText(frame, text, (10, 34),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 255, 255), 2)
    return frame


# ─── Main detection loop ───────────────────────────────────────────────────────
def run_detector():
    print("[DETECTOR] Loading model...")
    model = YOLO(MODEL_PATH)

    print(f"[DETECTOR] Opening video: {VIDEO_PATH}")
    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print(f"[DETECTOR] ERROR: Could not open {VIDEO_PATH}")
        return

    # init_db()

    frame_count = 0
    last_logged = {}
    classes_to_detect = list(CLASS_NAMES.keys())

    print("[DETECTOR] Running. Writing frames to stream...")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("[DETECTOR] Video ended — looping.")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame_count += 1
        violations_this_frame = []

        results = model.track(
            frame,
            conf=min(CLASS_CONF.values()),
            classes=classes_to_detect,
            verbose=False,
            persist=True,
            tracker="bytetrack.yaml"
        )

        detections = results[0].boxes

        if detections is not None:
            for box in detections:
                cls_id     = int(box.cls[0])
                confidence = float(box.conf[0])
                

                if confidence < CLASS_CONF.get(cls_id, CONF_THRESH):
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                x_center = (x1 + x2) // 2
                label    = CLASS_NAMES.get(cls_id, "Unknown")

                is_violation = cls_id in VIOLATION_CLASSES
                color = (0, 0, 220) if is_violation else (0, 200, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} {confidence:.2f}",
                            (x1, y1 - 28), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                
                if is_violation:
                    violation_name = VIOLATION_CLASSES[cls_id]
                    zone = get_zone(x_center, frame.shape[1])
                    now  = time.time()

                    if now - last_logged.get(violation_name, 0) > COOLDOWN:
                        snap = save_snapshot(frame, violation_name)
                        print("about to log violation")
                        log_violation(zone, violation_name, confidence, snap)
                        print("logged")
                        last_logged[violation_name] = now
                        print(f"[VIOLATION] {violation_name} | Zone: {zone} | Conf: {confidence:.2f}")


                    violations_this_frame.append(violation_name)

        frame = draw_violation_banner(frame, violations_this_frame)
        cv2.putText(frame, f"Frame {frame_count}", (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)

        frame_store.write(frame)

    cap.release()
    print("[DETECTOR] Stopped.")


if __name__ == "__main__":
    run_detector()