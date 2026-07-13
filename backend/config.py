import os
from dotenv import load_dotenv

load_dotenv() # loads everything from the .env file

# Paths
DB_PATH    = "backend/violations.db"
MODEL_PATH = "models/best.pt"
VIDEO_PATH = "demo_video.mp4"
SNAP_DIR   = "snapshots"

# API
API_BASE   = "http://localhost:8000"

# Detection
CONF_THRESH = 0.25
FRAME_SKIP  = 1
COOLDOWN    = 10  # seconds between logging same violation

CLASS_CONF = {
    0: 0.75,   # Hardhat
    2: 0.35,   # NO-Hardhat
    4: 0.35,   # NO-Safety Vest
    5: 0.40,   # Person
    7: 0.40,   # Safety Vest
}

ZONES = ["Entry Gate", "Scaffolding Area", "Material Yard", "Crane Zone", "Office Block"]

VIOLATION_CLASSES = {
    2: "No Hardhat",
    4: "No Safety Vest"
}

CLASS_NAMES = {
    0: "Hardhat",
    2: "NO-Hardhat",
    4: "NO-Safety Vest",
    5: "Person",
    7: "Safety Vest"
}