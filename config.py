# flask-pantilt-cam.py settings
# ===== CONFIGURATION VARIABLES =====

class Config:
    # Camera Settings
    IM_WIDTH = 800
    IM_HEIGHT = 400
    IM_HFLIP = True
    IM_VFLIP = True

    # Photo Settings
    IM_SNAP_WIDTH = 1920
    IM_SNAP_HEIGHT = 1080
    IM_SNAP_FILEPATH = "./images"
    IM_SNAP_PREFIX = "camshot"

    # Pan-Tilt Settings
    PAN_SPEED = 5
    TILT_SPEED = -5

    # Web Interface
    WEB_TITLE = "PiCamera Pan-Tilt Control"
    PHOTOS_PER_PAGE = 16

# ===================================