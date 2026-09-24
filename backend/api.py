import cv2
import time
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from backend.database import (
    init_db, get_violations, get_recent_violations,
    get_stats, get_zones, acknowledge_violation,
    clear_violations
)

# ─── Shared frame store ────────────────────────────────────────────────────────
class FrameStore:
    def __init__(self):
        self.frame = None
        self.lock  = threading.Lock()

    def write(self, frame):
        with self.lock:
            self.frame = frame.copy()

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

frame_store = FrameStore()

# ─── Startup ───────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app):
    from detection.detector import run_detector
    init_db()
    t = threading.Thread(target=run_detector, daemon=True)
    t.start()
    print("[API] SafeWatch API started + detector running")
    yield

app = FastAPI(title="SafeWatch API", version="2.0", lifespan=lifespan)
app.mount("/snapshots", StaticFiles(directory="snapshots"), name="snapshots")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Health ────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "SafeWatch API running", "version": "2.0"}


# ─── Video feed ────────────────────────────────────────────────────────────────
def generate_frames():
    while True:
        frame = frame_store.read()
        print(f"[STREAM] frame is None: {frame is None}")
        if frame is None:
            # send a blank frame if detector not running
            import numpy as np
            blank = np.zeros((480, 640, 3), dtype="uint8")
            cv2.putText(blank, "Detector not running", (120, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            frame = blank

        _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            buffer.tobytes() +
            b"\r\n"
        )
        time.sleep(0.03)


@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


# ─── Violations ────────────────────────────────────────────────────────────────
@app.get("/violations")
def get_violations_route(limit: int = 50, zone: str = None, violation: str = None):
    return get_violations(limit, zone, violation)


@app.get("/violations/stats")
def get_stats_route():
    return get_stats()


@app.get("/violations/recent")
def get_recent_route(since_id: int = 0):
    return get_recent_violations(since_id)


@app.post("/violations/{violation_id}/acknowledge")
def acknowledge_route(violation_id: int):
    acknowledge_violation(violation_id)
    return {"status": "acknowledged", "id": violation_id}


@app.delete("/violations/clear")
def clear_route():
    clear_violations()
    return {"status": "cleared"}


# ─── Zones ─────────────────────────────────────────────────────────────────────
@app.get("/zones")
def get_zones_route():
    return get_zones()





# ─── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.api:app", host="0.0.0.0", port=8000, reload=False)