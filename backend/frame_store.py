import threading

class FrameStore:
    def __init__(self):
        self.frame = None
        self.lock = threading.Lock()

    def write(self, frame):
        with self.lock:
            self.frame = frame.copy()

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

frame_store = FrameStore()